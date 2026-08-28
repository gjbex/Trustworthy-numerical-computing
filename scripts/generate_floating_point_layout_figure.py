#!/usr/bin/env python3
"""Generate a deterministic SVG of floating-point fields and byte order."""

from __future__ import annotations

from dataclasses import dataclass
import html
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = (
    REPOSITORY_ROOT / "figures" / "floating-point-layouts-little-endian.svg"
)

WIDTH = 1200
HEIGHT = 1060

NAVY = "#17324D"
PURPLE = "#CC79A7"
ORANGE = "#E69F00"
BLUE = "#0072B2"
GRAY = "#5F6B76"
LIGHT_GRAY = "#D9E1E8"
WHITE = "#FFFFFF"


@dataclass(frozen=True)
class FormatSpec:
    """Stored field widths for one binary floating-point format."""

    name: str
    total_bits: int
    exponent_bits: int
    fraction_bits: int

    @property
    def precision(self) -> int:
        """Return normal-number significand precision, including the leading bit."""

        return self.fraction_bits + 1


FORMATS = (
    FormatSpec("binary16", 16, 5, 10),
    FormatSpec("bfloat16", 16, 8, 7),
    FormatSpec("binary32", 32, 8, 23),
    FormatSpec("binary64", 64, 11, 52),
)


def text_element(
    x: float,
    y: float,
    content: str,
    *,
    size: int = 17,
    fill: str = NAVY,
    anchor: str = "start",
    weight: str = "400",
) -> str:
    """Return one escaped SVG text element."""

    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}">{html.escape(content)}</text>'
    )


def multiline_text(
    x: float,
    y: float,
    lines: tuple[str, ...],
    *,
    size: int,
    fill: str = NAVY,
    anchor: str = "middle",
    weight: str = "600",
    line_height: float = 1.18,
) -> str:
    """Return an escaped, centred multiline SVG text element."""

    spans = [
        f'<tspan x="{x:.1f}" dy="{0 if index == 0 else line_height:.2f}em">'
        f"{html.escape(line)}</tspan>"
        for index, line in enumerate(lines)
    ]
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}">{"".join(spans)}</text>'
    )


def line_element(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    stroke: str = NAVY,
    width: float = 1.0,
) -> str:
    """Return one SVG line element."""

    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}"/>'
    )


def field_for_bit(spec: FormatSpec, bit_index: int) -> tuple[str, str]:
    """Return the name and colour of the field containing one logical bit."""

    if bit_index == spec.total_bits - 1:
        return "S", PURPLE
    if bit_index >= spec.fraction_bits:
        return "E", ORANGE
    return "F", BLUE


def logical_layout(spec: FormatSpec, y: float) -> list[str]:
    """Draw the endian-independent logical layout for one format."""

    x = 220.0
    total_width = 920.0
    bar_height = 72.0
    bit_width = total_width / spec.total_bits
    fields = (
        (
            1,
            PURPLE,
            ("S",),
        ),
        (
            spec.exponent_bits,
            ORANGE,
            (
                "Exponent",
                f"{spec.exponent_bits} bits: {spec.total_bits - 2}…{spec.fraction_bits}",
            ),
        ),
        (
            spec.fraction_bits,
            BLUE,
            (
                "Stored fraction",
                f"{spec.fraction_bits} bits: {spec.fraction_bits - 1}…0",
            ),
        ),
    )

    elements = [
        text_element(48.0, y + 31.0, spec.name, size=20, weight="700"),
        text_element(
            48.0,
            y + 55.0,
            f"p = {spec.precision} for normal values",
            size=14,
            fill=GRAY,
        ),
    ]
    current_x = x
    for field_bits, colour, lines in fields:
        field_width = field_bits * bit_width
        elements.append(
            f'<rect x="{current_x:.1f}" y="{y:.1f}" width="{field_width:.1f}" '
            f'height="{bar_height:.1f}" fill="{colour}" stroke="{WHITE}" stroke-width="2"/>'
        )
        if field_bits == 1:
            elements.append(
                multiline_text(
                    current_x + field_width / 2.0,
                    y + 44.0,
                    lines,
                    size=18,
                    fill=WHITE,
                )
            )
        else:
            label_size = 15 if field_width < 180.0 else 16
            elements.append(
                multiline_text(
                    current_x + field_width / 2.0,
                    y + 29.0,
                    lines,
                    size=label_size,
                    fill=NAVY if colour == ORANGE else WHITE,
                )
            )
        current_x += field_width

    elements.extend(
        (
            text_element(x, y - 8.0, f"bit {spec.total_bits - 1}", size=13, fill=GRAY),
            text_element(x + total_width, y - 8.0, "bit 0", size=13, fill=GRAY, anchor="end"),
        )
    )
    return elements


def memory_layout(spec: FormatSpec, y: float) -> list[str]:
    """Draw low-to-high-address bytes for one little-endian stored value."""

    x = 220.0
    bit_width = 13.75
    bit_height = 36.0
    byte_width = bit_width * 8.0
    elements = [
        text_element(48.0, y + 25.0, spec.name, size=20, weight="700"),
        text_element(
            48.0,
            y + 48.0,
            f"{spec.total_bits // 8} bytes",
            size=14,
            fill=GRAY,
        ),
    ]

    for byte_index in range(spec.total_bits // 8):
        byte_x = x + byte_index * byte_width
        elements.append(
            text_element(
                byte_x + byte_width / 2.0,
                y - 9.0,
                "bits 7…0",
                size=12,
                fill=GRAY,
                anchor="middle",
            )
        )
        for offset, local_bit in enumerate(range(7, -1, -1)):
            logical_bit = byte_index * 8 + local_bit
            field_name, colour = field_for_bit(spec, logical_bit)
            bit_x = byte_x + offset * bit_width
            elements.append(
                f'<rect x="{bit_x:.1f}" y="{y:.1f}" width="{bit_width:.1f}" '
                f'height="{bit_height:.1f}" fill="{colour}" stroke="{WHITE}" '
                f'stroke-width="0.8"/>'
            )
            elements.append(
                text_element(
                    bit_x + bit_width / 2.0,
                    y + 24.0,
                    field_name,
                    size=11,
                    fill=NAVY if colour == ORANGE else WHITE,
                    anchor="middle",
                    weight="700",
                )
            )
        elements.append(
            f'<rect x="{byte_x:.1f}" y="{y:.1f}" width="{byte_width:.1f}" '
            f'height="{bit_height:.1f}" fill="none" stroke="{NAVY}" stroke-width="1.4"/>'
        )
        elements.append(
            text_element(
                byte_x + byte_width / 2.0,
                y + 57.0,
                f"byte +{byte_index}",
                size=13,
                anchor="middle",
                weight="600",
            )
        )

    return elements


def validate_specs() -> None:
    """Guard the reviewed field allocations used by the course."""

    expected = {
        "binary16": (16, 5, 10, 11),
        "bfloat16": (16, 8, 7, 8),
        "binary32": (32, 8, 23, 24),
        "binary64": (64, 11, 52, 53),
    }
    observed = {
        spec.name: (
            spec.total_bits,
            spec.exponent_bits,
            spec.fraction_bits,
            spec.precision,
        )
        for spec in FORMATS
    }
    if observed != expected:
        raise RuntimeError("floating-point field allocations differ from reviewed values")
    if any(1 + spec.exponent_bits + spec.fraction_bits != spec.total_bits for spec in FORMATS):
        raise RuntimeError("floating-point fields do not add up to the storage width")


def generate_svg() -> str:
    """Return the complete SVG document."""

    validate_specs()
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        "<title id=\"title\">Floating-point fields and little-endian byte order</title>",
        (
            "<desc id=\"description\">The first panel compares the logical sign, exponent, "
            "and stored fraction fields of binary16, bfloat16, binary32, and binary64. The "
            "second panel shows the same fields grouped into bytes in increasing memory "
            "address order on a little-endian system. Byte order changes, but bits within "
            "each byte are shown from bit seven to bit zero.</desc>"
        ),
        (
            "<metadata>Generated deterministically by "
            "scripts/generate_floating_point_layout_figure.py. Field widths follow IEEE "
            "754 binary16, binary32, and binary64, and the common bfloat16 layout.</metadata>"
        ),
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{WHITE}"/>',
        (
            '<style>text { font-family: system-ui, "Segoe UI", Arial, sans-serif; } '
            'line, rect { vector-effect: non-scaling-stroke; }</style>'
        ),
        text_element(48.0, 43.0, "Floating-point fields and little-endian byte order", size=29, weight="700"),
        text_element(
            48.0,
            73.0,
            "Field widths determine precision and range; byte order determines storage in memory",
            size=17,
            fill=GRAY,
        ),
        text_element(48.0, 116.0, "A  Logical field layout (endian-independent)", size=21, weight="700"),
        text_element(1140.0, 116.0, "most-significant bit at left; least-significant bit at right", size=14, fill=GRAY, anchor="end"),
    ]

    for spec, y in zip(FORMATS, (148.0, 240.0, 332.0, 424.0), strict=True):
        elements.extend(logical_layout(spec, y))

    elements.extend(
        (
            line_element(48.0, 518.0, 1152.0, 518.0, stroke=LIGHT_GRAY, width=2.0),
            text_element(48.0, 558.0, "B  Bytes in memory on a little-endian system", size=21, weight="700"),
            text_element(1140.0, 558.0, "lower address at left; higher address at right", size=14, fill=GRAY, anchor="end"),
            text_element(
                220.0,
                587.0,
                "Within each byte, the diagram uses the conventional bit 7 → bit 0 display.",
                size=14,
                fill=GRAY,
            ),
        )
    )

    for spec, y in zip(FORMATS, (620.0, 710.0, 800.0, 890.0), strict=True):
        elements.extend(memory_layout(spec, y))

    legend_y = 1000.0
    for x, label, colour in (
        (48.0, "S  sign", PURPLE),
        (190.0, "E  exponent", ORANGE),
        (370.0, "F  stored fraction", BLUE),
    ):
        elements.append(f'<rect x="{x:.1f}" y="{legend_y - 17:.1f}" width="24" height="24" fill="{colour}"/>')
        elements.append(text_element(x + 34.0, legend_y + 2.0, label, size=15, weight="600"))

    elements.extend(
        (
            text_element(
                1152.0,
                992.0,
                "For normal values, p = stored fraction bits + 1",
                size=14,
                fill=GRAY,
                anchor="end",
            ),
            text_element(
                1152.0,
                1015.0,
                "The extra leading significand bit is implicit, not stored.",
                size=14,
                fill=GRAY,
                anchor="end",
            ),
            text_element(
                48.0,
                1043.0,
                "Little endian reverses byte significance in memory; it does not reverse all bits.",
                size=17,
                fill=NAVY,
                weight="700",
            ),
            "</svg>",
        )
    )
    return "\n".join(elements) + "\n"


def main() -> None:
    """Write the figure to its documented repository location."""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(generate_svg(), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
