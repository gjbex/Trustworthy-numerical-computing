#!/usr/bin/env python3
"""Generate the reviewed two-equation sensitivity figure as deterministic SVG."""

from __future__ import annotations

from decimal import Decimal
import html
import math
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPOSITORY_ROOT / "figures" / "two-equation-sensitivity.svg"

WIDTH = 1200
HEIGHT = 850

NAVY = "#17324D"
BLUE = "#0072B2"
ORANGE = "#D55E00"
PURPLE = "#8E5AA7"
GRAY = "#5F6B76"
LIGHT_GRAY = "#D9E1E8"
PALE_BLUE = "#F2F8FC"
PALE_ORANGE = "#FFF7F0"
WHITE = "#FFFFFF"

PLOT_TOP = 150.0
PLOT_SIZE = 380.0
LEFT_PLOT = 105.0
RIGHT_PLOT = 700.0


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
    size: int = 16,
    fill: str = NAVY,
    anchor: str = "middle",
    weight: str = "400",
    line_height: float = 1.25,
) -> str:
    """Return an escaped multiline SVG text element."""

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
    stroke: str,
    width: float = 1.0,
    dash: str | None = None,
    marker_end: str | None = None,
) -> str:
    """Return one SVG line element."""

    dash_attribute = f' stroke-dasharray="{dash}"' if dash else ""
    marker_attribute = f' marker-end="url(#{marker_end})"' if marker_end else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}"{dash_attribute}'
        f'{marker_attribute}/>'
    )


def map_x(plot_left: float, x1: float) -> float:
    """Map x1 from the shared range [0, 2] to one plot."""

    return plot_left + (x1 / 2.0) * PLOT_SIZE


def map_y(x2: float) -> float:
    """Map x2 from the shared range [0, 2] to one plot."""

    return PLOT_TOP + (1.0 - x2 / 2.0) * PLOT_SIZE


def crossing_angle_degrees(delta: float) -> float:
    """Return the acute angle between the two equation lines."""

    first_angle = math.atan(-1.0)
    second_angle = math.atan(-1.0 / (1.0 + delta))
    return abs(first_angle - second_angle) * 180.0 / math.pi


def equation_panel(
    *,
    plot_left: float,
    delta: float,
    title: str,
    angle_label: str,
) -> list[str]:
    """Draw the two equations on a common x1-x2 coordinate scale."""

    elements = [
        text_element(
            plot_left + PLOT_SIZE / 2.0,
            132.0,
            title,
            size=23,
            anchor="middle",
            weight="700",
        ),
        f'<rect x="{plot_left:.1f}" y="{PLOT_TOP:.1f}" width="{PLOT_SIZE:.1f}" '
        f'height="{PLOT_SIZE:.1f}" fill="{PALE_BLUE}" stroke="{NAVY}" '
        f'stroke-width="1.5"/>',
    ]

    for tick in (0.0, 1.0, 2.0):
        x = map_x(plot_left, tick)
        y = map_y(tick)
        elements.extend(
            (
                line_element(x, PLOT_TOP, x, PLOT_TOP + PLOT_SIZE, stroke=LIGHT_GRAY),
                line_element(plot_left, y, plot_left + PLOT_SIZE, y, stroke=LIGHT_GRAY),
                text_element(x, PLOT_TOP + PLOT_SIZE + 25.0, f"{tick:.0f}", size=14, anchor="middle"),
                text_element(plot_left - 13.0, y + 5.0, f"{tick:.0f}", size=14, anchor="end"),
            )
        )

    equation_1 = (
        map_x(plot_left, 0.0),
        map_y(2.0),
        map_x(plot_left, 2.0),
        map_y(0.0),
    )
    equation_2 = (
        map_x(plot_left, 0.0),
        map_y((2.0 + delta) / (1.0 + delta)),
        map_x(plot_left, 2.0),
        map_y(delta / (1.0 + delta)),
    )
    elements.extend(
        (
            line_element(*equation_1, stroke=BLUE, width=3.2),
            line_element(*equation_2, stroke=ORANGE, width=3.2, dash="10 7"),
            f'<circle cx="{map_x(plot_left, 1.0):.1f}" cy="{map_y(1.0):.1f}" '
            f'r="6.0" fill="{PURPLE}" stroke="{WHITE}" stroke-width="2"/>',
            text_element(
                map_x(plot_left, 1.0) + 12.0,
                map_y(1.0) - 12.0,
                "x = (1, 1)",
                size=15,
                weight="600",
            ),
            text_element(
                plot_left + PLOT_SIZE / 2.0,
                PLOT_TOP + 28.0,
                angle_label,
                size=15,
                fill=GRAY,
                anchor="middle",
                weight="600",
            ),
            text_element(
                plot_left + PLOT_SIZE / 2.0,
                PLOT_TOP + PLOT_SIZE + 54.0,
                "x1",
                size=17,
                anchor="middle",
                weight="600",
            ),
            text_element(
                plot_left - 44.0,
                PLOT_TOP + PLOT_SIZE / 2.0,
                "x2",
                size=17,
                anchor="middle",
                weight="600",
            ),
        )
    )
    return elements


def displacement_card(
    *,
    x: float,
    title: str,
    target_label: tuple[str, ...],
    displacement: str,
    fill: str,
) -> list[str]:
    """Draw one independently magnified solution-displacement indicator."""

    y = 645.0
    card_width = 485.0
    start_x = x + 65.0
    end_x = x + 365.0
    arrow_y = y + 63.0
    return [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{card_width:.1f}" height="145" '
        f'rx="10" fill="{fill}" stroke="{LIGHT_GRAY}" stroke-width="1.5"/>',
        text_element(x + 20.0, y + 30.0, title, size=19, weight="700"),
        line_element(start_x, arrow_y, end_x, arrow_y, stroke=PURPLE, width=3.0, marker_end="arrow"),
        f'<circle cx="{start_x:.1f}" cy="{arrow_y:.1f}" r="6" fill="{NAVY}"/>',
        f'<circle cx="{end_x:.1f}" cy="{arrow_y:.1f}" r="6" fill="{PURPLE}"/>',
        text_element(start_x, arrow_y - 15.0, "baseline x = (1, 1)", size=14, anchor="middle"),
        multiline_text(end_x, arrow_y - 38.0, target_label, size=14, anchor="middle", weight="600"),
        text_element(
            x + card_width / 2.0,
            y + 128.0,
            displacement,
            size=16,
            fill=PURPLE,
            anchor="middle",
            weight="700",
        ),
    ]


def validate_values() -> None:
    """Guard the exact values and geometric annotations used in the figure."""

    eta = Decimal("1e-16")
    deltas = (Decimal("1"), Decimal("1e-12"))
    displacements = tuple(eta / delta for delta in deltas)
    if displacements != (Decimal("1e-16"), Decimal("1e-4")):
        raise RuntimeError("reviewed solution displacements have changed")

    angles = tuple(crossing_angle_degrees(float(delta)) for delta in deltas)
    if not math.isclose(angles[0], 18.43494882292201, rel_tol=1.0e-14):
        raise RuntimeError("reviewed delta=1 crossing angle has changed")
    if not (2.86e-11 <= angles[1] <= 2.87e-11):
        raise RuntimeError("reviewed near-parallel crossing angle has changed")


def generate_svg() -> str:
    """Return the complete SVG document."""

    validate_values()
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        "<title id=\"title\">Geometry of the two-equation sensitivity experiment</title>",
        (
            "<desc id=\"description\">Two coordinate-plane panels compare the lines "
            "defined by the Module 4 equations for delta equal to one and delta equal "
            "to ten to the minus twelve. The first pair crosses visibly; the second is "
            "visually coincident at the same scale. Independently magnified arrows show "
            "that the same right-hand-side perturbation moves the solution by ten to the "
            "minus sixteen and ten to the minus four, respectively.</desc>"
        ),
        (
            "<metadata>Generated deterministically by "
            "scripts/generate_two_equation_sensitivity_figure.py from the exact "
            "dimensionless equations and eta=1e-16. The coordinate panels share linear "
            "axes from zero to two. Displacement arrows use independent magnification.</metadata>"
        ),
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{WHITE}"/>',
        (
            '<style>text { font-family: system-ui, "Segoe UI", Arial, sans-serif; } '
            'line, rect, circle { vector-effect: non-scaling-stroke; }</style>'
        ),
        (
            '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" '
            'refY="4" orient="auto"><path d="M 0 0 L 10 4 L 0 8 z" '
            f'fill="{PURPLE}"/></marker></defs>'
        ),
        text_element(55.0, 43.0, "Nearly parallel equations amplify the same input change", size=29, weight="700"),
        text_element(
            55.0,
            73.0,
            "Both coordinate panels use the same linear x1 and x2 scales",
            size=17,
            fill=GRAY,
        ),
        line_element(370.0, 103.0, 440.0, 103.0, stroke=BLUE, width=3.2),
        text_element(450.0, 109.0, "Equation 1: x1 + x2 = 2", size=15),
        line_element(690.0, 103.0, 760.0, 103.0, stroke=ORANGE, width=3.2, dash="10 7"),
        text_element(770.0, 109.0, "Equation 2: x1 + (1 + δ)x2 = 2 + δ", size=15),
    ]

    elements.extend(
        equation_panel(
            plot_left=LEFT_PLOT,
            delta=1.0,
            title="δ = 1",
            angle_label="crossing angle ≈ 18.4°",
        )
    )
    elements.extend(
        equation_panel(
            plot_left=RIGHT_PLOT,
            delta=1.0e-12,
            title="δ = 1e-12",
            angle_label="angle ≈ 2.86e-11°: visually coincident",
        )
    )

    elements.extend(
        (
            text_element(
                WIDTH / 2.0,
                602.0,
                "Same RHS-input perturbation Δb = (0, 1e-16)",
                size=20,
                anchor="middle",
                weight="700",
            ),
            text_element(
                WIDTH / 2.0,
                626.0,
                "Solution-displacement arrows below are independently magnified",
                size=15,
                fill=GRAY,
                anchor="middle",
            ),
        )
    )
    elements.extend(
        displacement_card(
            x=80.0,
            title="δ = 1",
            target_label=("perturbed x", "(1 - 1e-16, 1 + 1e-16)"),
            displacement="max |Δx_i| = 1e-16",
            fill=PALE_BLUE,
        )
    )
    elements.extend(
        displacement_card(
            x=635.0,
            title="δ = 1e-12",
            target_label=("perturbed x", "(0.9999, 1.0001)"),
            displacement="max |Δx_i| = 1e-4",
            fill=PALE_ORANGE,
        )
    )
    elements.extend(
        (
            text_element(
                WIDTH / 2.0,
                828.0,
                "The solution change is 1e12 times larger when the equations are nearly dependent.",
                size=18,
                anchor="middle",
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
