#!/usr/bin/env python3
"""Generate the reviewed binary64-spacing course figure as deterministic SVG."""

from __future__ import annotations

import html
import math
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPOSITORY_ROOT / "figures" / "binary64-spacing.svg"

WIDTH = 1120
HEIGHT = 800

PLOT_LEFT = 110.0
PLOT_RIGHT = 1060.0
PLOT_TOP = 110.0
PLOT_BOTTOM = 450.0

LOG_X_MIN = -6.5
LOG_X_MAX = 16.5
LOG_GAP_MIN = -23.0
LOG_GAP_MAX = 1.5

NAVY = "#17324D"
BLUE = "#0072B2"
ORANGE = "#D55E00"
GRAY = "#5F6B76"
LIGHT_GRAY = "#D9E1E8"
PALE_BLUE = "#EAF4FA"
WHITE = "#FFFFFF"


def map_x(log_value: float) -> float:
    """Map a base-10 logarithm of magnitude to the plot x coordinate."""

    fraction = (log_value - LOG_X_MIN) / (LOG_X_MAX - LOG_X_MIN)
    return PLOT_LEFT + fraction * (PLOT_RIGHT - PLOT_LEFT)


def map_y(log_gap: float) -> float:
    """Map a base-10 logarithm of spacing to the plot y coordinate."""

    fraction = (log_gap - LOG_GAP_MIN) / (LOG_GAP_MAX - LOG_GAP_MIN)
    return PLOT_BOTTOM - fraction * (PLOT_BOTTOM - PLOT_TOP)


def text_element(
    x: float,
    y: float,
    content: str,
    *,
    size: int = 17,
    fill: str = NAVY,
    anchor: str = "start",
    weight: str = "400",
    transform: str | None = None,
) -> str:
    """Return one escaped SVG text element."""

    transform_attribute = f' transform="{transform}"' if transform else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"'
        f'{transform_attribute}>{html.escape(content)}</text>'
    )


def line_element(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    stroke: str,
    width: float = 1.0,
    dash: str | None = None,
) -> str:
    """Return one SVG line element."""

    dash_attribute = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}"{dash_attribute}/>'
    )


def binary64_upward_gap(value: float) -> float:
    """Return the upward gap from a finite positive binary64 value."""

    if not math.isfinite(value) or value <= 0.0:
        raise ValueError("value must be finite and positive")
    return math.nextafter(value, math.inf) - value


def staircase_path() -> str:
    """Build the exact normal-range staircase over the displayed magnitudes."""

    minimum_value = 10.0**LOG_X_MIN
    maximum_value = 10.0**LOG_X_MAX
    first_exponent = math.floor(math.log2(minimum_value))
    last_exponent = math.floor(math.log2(maximum_value))

    commands: list[str] = []
    for exponent in range(first_exponent, last_exponent + 1):
        interval_start = max(minimum_value, 2.0**exponent)
        interval_end = min(maximum_value, 2.0 ** (exponent + 1))
        if interval_start >= interval_end:
            continue

        gap = 2.0 ** (exponent - 52)
        x_start = map_x(math.log10(interval_start))
        x_end = map_x(math.log10(interval_end))
        y = map_y(math.log10(gap))

        if not commands:
            commands.append(f"M {x_start:.1f} {y:.1f}")
        else:
            commands.append(f"L {x_start:.1f} {y:.1f}")
        commands.append(f"L {x_end:.1f} {y:.1f}")

        if interval_end < maximum_value:
            next_gap = 2.0 ** (exponent - 51)
            next_y = map_y(math.log10(next_gap))
            commands.append(f"L {x_end:.1f} {next_y:.1f}")

    return " ".join(commands)


def local_number_line(
    *,
    label: str,
    y: float,
    tick_labels: tuple[str, str, str],
    gap_label: str,
) -> list[str]:
    """Build one separately magnified local floating-point number line."""

    line_start = 350.0
    tick_positions = (440.0, 700.0, 960.0)
    line_end = 1030.0
    elements = [
        text_element(95.0, y + 6.0, label, size=19, weight="600"),
        line_element(line_start, y, line_end, y, stroke=NAVY, width=2.5),
        line_element(
            tick_positions[0],
            y - 27.0,
            tick_positions[1],
            y - 27.0,
            stroke=ORANGE,
            width=2.0,
        ),
        text_element(
            (tick_positions[0] + tick_positions[1]) / 2.0,
            y - 38.0,
            gap_label,
            size=16,
            fill=ORANGE,
            anchor="middle",
            weight="600",
        ),
    ]

    for position, tick_label in zip(tick_positions, tick_labels, strict=True):
        elements.append(
            line_element(position, y - 13.0, position, y + 13.0, stroke=BLUE, width=3.0)
        )
        elements.append(
            text_element(position, y + 38.0, tick_label, size=16, anchor="middle")
        )

    return elements


def generate_svg() -> str:
    """Return the complete SVG document."""

    reference_points = (
        (1.0e-6, "10⁻⁶", 30.0, -16.0),
        (1.0, "1", 0.0, -17.0),
        (1.0e6, "10⁶", 0.0, -17.0),
        (float(2**53), "2⁵³", -33.0, -18.0),
        (1.0e16, "10¹⁶", 38.0, 24.0),
    )

    expected_gaps = (2.117582368135751e-22, 2.220446049250313e-16, 1.1641532182693481e-10, 2.0, 2.0)
    observed_gaps = tuple(binary64_upward_gap(point[0]) for point in reference_points)
    if observed_gaps != expected_gaps:
        raise RuntimeError("binary64 reference gaps differ from the reviewed values")

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        "<title id=\"title\">Binary64 spacing grows with magnitude</title>",
        (
            "<desc id=\"description\">A logarithmic staircase plot shows the upward gap "
            "between adjacent positive binary64 numbers from ten to the minus six through "
            "ten to the sixteen. The gap rises from about two times ten to the minus "
            "twenty-two to two. Separately magnified number lines compare spacing near "
            "one with spacing near two to the fifty-three.</desc>"
        ),
        (
            "<metadata>Generated deterministically by "
            "scripts/generate_binary64_spacing_figure.py using Python math.nextafter. "
            "The plotted values are finite positive IEEE 754 binary64 values.</metadata>"
        ),
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{WHITE}"/>',
        (
            '<style>text { font-family: system-ui, "Segoe UI", Arial, sans-serif; } '
            'path, line, circle { vector-effect: non-scaling-stroke; }</style>'
        ),
        text_element(55.0, 43.0, "Binary64 spacing grows with magnitude", size=29, weight="700"),
        text_element(
            55.0,
            73.0,
            "Upward gap to the next representable positive value; both axes are logarithmic",
            size=17,
            fill=GRAY,
        ),
        f'<rect x="{PLOT_LEFT:.1f}" y="{PLOT_TOP:.1f}" '
        f'width="{PLOT_RIGHT - PLOT_LEFT:.1f}" height="{PLOT_BOTTOM - PLOT_TOP:.1f}" '
        f'fill="{PALE_BLUE}" stroke="{NAVY}" stroke-width="1.5"/>',
    ]

    x_ticks = ((-6.0, "10⁻⁶"), (0.0, "1"), (6.0, "10⁶"), (12.0, "10¹²"), (16.0, "10¹⁶"))
    for log_value, label in x_ticks:
        x = map_x(log_value)
        elements.append(line_element(x, PLOT_TOP, x, PLOT_BOTTOM, stroke=LIGHT_GRAY, width=1.0))
        elements.append(line_element(x, PLOT_BOTTOM, x, PLOT_BOTTOM + 8.0, stroke=NAVY, width=1.5))
        elements.append(text_element(x, PLOT_BOTTOM + 31.0, label, size=16, anchor="middle"))

    y_ticks = ((-22.0, "10⁻²²"), (-16.0, "10⁻¹⁶"), (-10.0, "10⁻¹⁰"), (-4.0, "10⁻⁴"), (0.0, "1"))
    for log_gap, label in y_ticks:
        y = map_y(log_gap)
        elements.append(line_element(PLOT_LEFT, y, PLOT_RIGHT, y, stroke=LIGHT_GRAY, width=1.0))
        elements.append(line_element(PLOT_LEFT - 8.0, y, PLOT_LEFT, y, stroke=NAVY, width=1.5))
        elements.append(text_element(PLOT_LEFT - 16.0, y + 6.0, label, size=16, anchor="end"))

    elements.extend(
        (
            text_element(
                (PLOT_LEFT + PLOT_RIGHT) / 2.0,
                PLOT_BOTTOM + 68.0,
                "Value magnitude |x|",
                size=18,
                anchor="middle",
                weight="600",
            ),
            text_element(
                29.0,
                (PLOT_TOP + PLOT_BOTTOM) / 2.0,
                "Upward spacing",
                size=18,
                anchor="middle",
                weight="600",
                transform=f"rotate(-90 29.0 {(PLOT_TOP + PLOT_BOTTOM) / 2.0:.1f})",
            ),
            f'<path d="{staircase_path()}" fill="none" stroke="{BLUE}" '
            'stroke-width="3.2" stroke-linejoin="miter"/>',
        )
    )

    for value, label, label_dx, label_dy in reference_points:
        gap = binary64_upward_gap(value)
        x = map_x(math.log10(value))
        y = map_y(math.log10(gap))
        label_x = x + label_dx
        label_y = y + label_dy
        if label_dx or label_dy:
            elements.append(line_element(x, y, label_x, label_y + 5.0, stroke=ORANGE, width=1.2))
        elements.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.8" fill="{ORANGE}" stroke="{WHITE}" stroke-width="2"/>')
        elements.append(text_element(label_x, label_y, label, size=16, fill=ORANGE, anchor="middle", weight="700"))

    elements.extend(
        (
            text_element(55.0, 570.0, "Separately magnified local number lines", size=21, weight="700"),
            text_element(
                55.0,
                595.0,
                "Equal drawn distances below do not imply equal numerical gaps.",
                size=16,
                fill=GRAY,
            ),
        )
    )
    elements.extend(
        local_number_line(
            label="Near 1",
            y=645.0,
            tick_labels=("1", "1 + 2⁻⁵²", "1 + 2×2⁻⁵²"),
            gap_label="gap = 2⁻⁵² ≈ 2.22×10⁻¹⁶",
        )
    )
    elements.extend(
        local_number_line(
            label="Near 2⁵³",
            y=735.0,
            tick_labels=("2⁵³", "2⁵³ + 2", "2⁵³ + 4"),
            gap_label="gap = 2",
        )
    )

    elements.append("</svg>")
    return "\n".join(elements) + "\n"


def main() -> None:
    """Write the generated SVG to the reviewed course-asset location."""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(generate_svg(), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
    main()
