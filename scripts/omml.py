#!/usr/bin/env python3
"""Small, deterministic LaTeX-to-OMML converter for thesis formulas.

The converter intentionally supports the constructs most common in Chinese
engineering theses and fails loudly for unsupported commands. It emits native
Word OMML, never an image or italicized plain text.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from lxml import etree

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
M = lambda name: f"{{{M_NS}}}{name}"
W = lambda name: f"{{{W_NS}}}{name}"


GREEK = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "epsilon": "ϵ",
    "varepsilon": "ε",
    "zeta": "ζ",
    "eta": "η",
    "theta": "θ",
    "vartheta": "ϑ",
    "iota": "ι",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "xi": "ξ",
    "pi": "π",
    "varpi": "ϖ",
    "rho": "ρ",
    "sigma": "σ",
    "tau": "τ",
    "upsilon": "υ",
    "phi": "ϕ",
    "varphi": "φ",
    "chi": "χ",
    "psi": "ψ",
    "omega": "ω",
    "Gamma": "Γ",
    "Delta": "Δ",
    "Theta": "Θ",
    "Lambda": "Λ",
    "Xi": "Ξ",
    "Pi": "Π",
    "Sigma": "Σ",
    "Upsilon": "Υ",
    "Phi": "Φ",
    "Psi": "Ψ",
    "Omega": "Ω",
}

SYMBOLS = {
    "cdot": "·",
    "times": "×",
    "pm": "±",
    "mp": "∓",
    "le": "≤",
    "leq": "≤",
    "ge": "≥",
    "geq": "≥",
    "neq": "≠",
    "approx": "≈",
    "propto": "∝",
    "infty": "∞",
    "to": "→",
    "rightarrow": "→",
    "leftarrow": "←",
    "ldots": "…",
    "dots": "…",
    "in": "∈",
}

OPERATORS = {"sum": "∑", "prod": "∏", "int": "∫", "lim": "lim", "max": "max", "min": "min"}
UPRIGHT_COMMANDS = {"mathrm", "text", "operatorname", "mathbf", "mathit"}
UNICODE_SUBSCRIPTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ", "0123456789aehijkl mnoprstuvx".replace(" ", ""))
UNICODE_SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ", "0123456789+-=()ni")


@dataclass
class Atom:
    text: str
    italic: bool = True


@dataclass
class Group:
    children: list[object]


@dataclass
class Fraction:
    numerator: object
    denominator: object


@dataclass
class Radical:
    content: object


@dataclass
class Script:
    base: object
    subscript: object | None = None
    superscript: object | None = None


@dataclass
class Accent:
    content: object
    accent: str


class LatexError(ValueError):
    """Raised when a formula cannot be safely converted."""


class Parser:
    def __init__(self, source: str):
        self.source = source.strip()
        self.pos = 0

    def parse(self, stop: str | None = None) -> list[object]:
        nodes: list[object] = []
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if stop and char == stop:
                self.pos += 1
                break
            if char == "}":
                if stop:
                    break
                raise LatexError("unmatched closing brace")
            if char.isspace():
                self.pos += 1
                continue
            if char == "{":
                self.pos += 1
                nodes.append(Group(self.parse("}")))
                continue
            if char in "_^":
                if not nodes:
                    raise LatexError(f"script {char!r} has no base")
                self.pos += 1
                script = self.argument()
                previous = nodes.pop()
                if isinstance(previous, Script):
                    if char == "_":
                        previous.subscript = script
                    else:
                        previous.superscript = script
                    nodes.append(previous)
                else:
                    nodes.append(
                        Script(
                            previous,
                            subscript=script if char == "_" else None,
                            superscript=script if char == "^" else None,
                        )
                    )
                continue
            if ord(char) in UNICODE_SUBSCRIPTS:
                if not nodes:
                    raise LatexError(f"subscript {char!r} has no base")
                previous = nodes.pop()
                value = Atom(char.translate(UNICODE_SUBSCRIPTS), italic=True)
                if isinstance(previous, Script) and previous.subscript is None:
                    previous.subscript = value
                    nodes.append(previous)
                else:
                    nodes.append(Script(previous, subscript=value))
                self.pos += 1
                continue
            if ord(char) in UNICODE_SUPERSCRIPTS:
                if not nodes:
                    raise LatexError(f"superscript {char!r} has no base")
                previous = nodes.pop()
                value = Atom(char.translate(UNICODE_SUPERSCRIPTS), italic=False)
                if isinstance(previous, Script) and previous.superscript is None:
                    previous.superscript = value
                    nodes.append(previous)
                else:
                    nodes.append(Script(previous, superscript=value))
                self.pos += 1
                continue
            if char == "\\":
                nodes.append(self.command())
                continue
            if char in "&":
                self.pos += 1
                continue
            if char in "(),.;:=+-*/<>[]|≤≥≠≈×·∑∏∫":
                self.pos += 1
                nodes.append(Atom(char, italic=False))
                continue
            if char.isdigit():
                start = self.pos
                while self.pos < len(self.source) and (
                    self.source[self.pos].isdigit() or self.source[self.pos] == "."
                ):
                    self.pos += 1
                nodes.append(Atom(self.source[start : self.pos], italic=False))
                continue
            if char.isalpha():
                self.pos += 1
                nodes.append(Atom(char, italic=True))
                continue
            raise LatexError(f"unsupported character {char!r} at position {self.pos}")
        else:
            if stop:
                raise LatexError(f"missing closing delimiter {stop!r}")
        return nodes

    def argument(self) -> object:
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            self.pos += 1
        if self.pos >= len(self.source):
            raise LatexError("missing script argument")
        if self.source[self.pos] == "{":
            self.pos += 1
            return Group(self.parse("}"))
        if self.source[self.pos] == "\\":
            return self.command()
        char = self.source[self.pos]
        self.pos += 1
        return Atom(char, italic=char.isalpha())

    def read_command(self) -> str:
        if self.pos >= len(self.source) or self.source[self.pos] != "\\":
            raise LatexError("expected command")
        self.pos += 1
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isalpha():
            self.pos += 1
        if start == self.pos:
            if self.pos >= len(self.source):
                raise LatexError("trailing backslash")
            command = self.source[self.pos]
            self.pos += 1
            return command
        return self.source[start : self.pos]

    def command(self) -> object:
        command = self.read_command()
        if command in {"left", "right"}:
            if self.pos >= len(self.source):
                raise LatexError(f"\\{command} has no delimiter")
            delimiter = self.source[self.pos]
            self.pos += 1
            return Atom(delimiter, italic=False)
        if command == "frac":
            return Fraction(self.argument(), self.argument())
        if command == "sqrt":
            if self.pos < len(self.source) and self.source[self.pos] == "[":
                end = self.source.find("]", self.pos)
                if end == -1:
                    raise LatexError("unterminated sqrt index")
                self.pos = end + 1
            return Radical(self.argument())
        if command in GREEK:
            return Atom(GREEK[command], italic=True)
        if command in SYMBOLS:
            return Atom(SYMBOLS[command], italic=False)
        if command in OPERATORS:
            return Atom(OPERATORS[command], italic=False)
        if command in UPRIGHT_COMMANDS:
            value = self.argument()
            return self.as_upright(value)
        if command == "begin":
            environment = self.argument()
            if isinstance(environment, Group):
                name = "".join(self.flatten_text(environment.children))
                if name not in {"aligned", "matrix", "pmatrix", "cases"}:
                    raise LatexError(f"unsupported environment {name!r}")
                content = self.parse_environment(name)
                return Group(content)
        if command in {"quad", "qquad", ",", " "}:
            return Atom(" ", italic=False)
        if command in {"{", "}"}:
            return Atom(command, italic=False)
        if command == "bar":
            return Accent(self.argument(), "\u0304")
        if command == "hat":
            return Accent(self.argument(), "\u0302")
        raise LatexError(f"unsupported LaTeX command '\\{command}'")

    def parse_environment(self, name: str) -> list[object]:
        marker = f"\\end{{{name}}}"
        end = self.source.find(marker, self.pos)
        if end == -1:
            raise LatexError(f"missing \\end{{{name}}}")
        content = self.source[self.pos : end]
        self.pos = end + len(marker)
        rows = re.split(r"\\\\", content)
        result: list[object] = []
        for index, row in enumerate(rows):
            result.extend(Parser(row).parse())
            if index < len(rows) - 1:
                result.append(Atom(" ", italic=False))
        return result

    def as_upright(self, value: object) -> object:
        if isinstance(value, Atom):
            return Atom(value.text, italic=False)
        if isinstance(value, Group):
            return Group([self.as_upright(item) for item in value.children])
        return value

    def flatten_text(self, nodes: Iterable[object]) -> list[str]:
        values: list[str] = []
        for node in nodes:
            if isinstance(node, Atom):
                values.append(node.text)
            elif isinstance(node, Group):
                values.extend(self.flatten_text(node.children))
        return values


def _run(text: str, italic: bool, size: int | None = None) -> etree._Element:
    run = etree.Element(M("r"))
    rpr = etree.SubElement(run, M("rPr"))
    sty = etree.SubElement(rpr, M("sty"))
    sty.set(M("val"), "i" if italic else "p")
    if size:
        word_rpr = etree.SubElement(run, W("rPr"))
        etree.SubElement(word_rpr, W("sz")).set(W("val"), str(size))
        etree.SubElement(word_rpr, W("szCs")).set(W("val"), str(size))
    text_node = etree.SubElement(run, M("t"))
    text_node.set(f"{{{XML_NS}}}space", "preserve")
    text_node.text = text
    return run


def _element(children: Iterable[etree._Element]) -> etree._Element:
    element = etree.Element(M("e"))
    for child in children:
        element.append(child)
    return element


def _render_contents(parent: etree._Element, node: object, size: int | None) -> None:
    if isinstance(node, Atom):
        parent.append(_run(node.text, node.italic, size))
        return
    if isinstance(node, Group):
        for child in node.children:
            _render_contents(parent, child, size)
        return
    if isinstance(node, Fraction):
        fraction = etree.Element(M("f"))
        etree.SubElement(fraction, M("fPr"))
        numerator = etree.SubElement(fraction, M("num"))
        _render_contents(numerator, node.numerator, size)
        denominator = etree.SubElement(fraction, M("den"))
        _render_contents(denominator, node.denominator, size)
        parent.append(fraction)
        return
    if isinstance(node, Radical):
        radical = etree.Element(M("rad"))
        rad_pr = etree.SubElement(radical, M("radPr"))
        etree.SubElement(rad_pr, M("degHide")).set(M("val"), "1")
        content = etree.SubElement(radical, M("e"))
        _render_contents(content, node.content, size)
        parent.append(radical)
        return
    if isinstance(node, Accent):
        accent = etree.Element(M("acc"))
        acc_pr = etree.SubElement(accent, M("accPr"))
        chr_el = etree.SubElement(acc_pr, M("chr"))
        chr_el.set(M("val"), node.accent)
        content = etree.SubElement(accent, M("e"))
        _render_contents(content, node.content, size)
        parent.append(accent)
        return
    if isinstance(node, Script):
        if node.subscript is not None and node.superscript is not None:
            script = etree.Element(M("sSubSup"))
            etree.SubElement(script, M("sSubSupPr"))
            base_tag, sub_tag, sup_tag = M("e"), M("sub"), M("sup")
        elif node.subscript is not None:
            script = etree.Element(M("sSub"))
            etree.SubElement(script, M("sSubPr"))
            base_tag, sub_tag, sup_tag = M("e"), M("sub"), None
        else:
            script = etree.Element(M("sSup"))
            etree.SubElement(script, M("sSupPr"))
            base_tag, sub_tag, sup_tag = M("e"), None, M("sup")
        base = etree.SubElement(script, base_tag)
        _render_contents(base, node.base, size)
        if sub_tag is not None:
            sub = etree.SubElement(script, sub_tag)
            _render_contents(sub, node.subscript, size)
        if sup_tag is not None:
            sup = etree.SubElement(script, sup_tag)
            _render_contents(sup, node.superscript, size)
        parent.append(script)
        return
    raise LatexError(f"cannot render node {node!r}")


def _render_node(node: object, size: int | None) -> etree._Element:
    element = etree.Element(M("e"))
    _render_contents(element, node, size)
    return element


def latex_to_omml(latex: str, *, display: bool = False, size: int | None = None) -> etree._Element:
    """Convert supported LaTeX into an inline or display OMML element."""
    nodes = Parser(latex).parse()
    math = etree.Element(M("oMath"))
    for node in nodes:
        _render_contents(math, node, size)
    if display:
        container = etree.Element(M("oMathPara"))
        container.append(math)
        return container
    return math


def omml_text(element: etree._Element) -> str:
    """Return the visible math text for duplicate and smoke checks."""
    return "".join(element.itertext())


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Convert common LaTeX to native Word OMML.")
    parser.add_argument("latex", nargs="?")
    parser.add_argument("--display", action="store_true")
    parser.add_argument("--size", type=int)
    args = parser.parse_args()
    if args.latex is None:
        parser.error("a LaTeX expression is required")
    element = latex_to_omml(args.latex, display=args.display, size=args.size)
    print(etree.tostring(element, encoding="unicode"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
