"""Reference implementation for the Module 10 sensor-inversion capstone."""

from __future__ import annotations

import argparse
import json
import math
import platform
import struct
from dataclasses import asdict, dataclass
from decimal import Decimal, localcontext


@dataclass(frozen=True)
class SensorCase:
    """Declared inputs and decision requirements for the teaching case."""

    y1: float = 1.0
    y2: float = 1.0000004
    separation: float = 1.0e-6
    reading_bound: float = 5.0e-8
    threshold_mg_per_l: float = 0.61
    required_accuracy_mg_per_l: float = 0.01


@dataclass(frozen=True)
class ConcentrationEnvelope:
    """Deterministic output bounds induced by bounded sensor readings."""

    c_a_min: float
    c_a_max: float
    c_b_min: float
    c_b_max: float
    total_min: float
    total_max: float


def binary32(value: float) -> float:
    """Round a Python float to IEEE 754 binary32 and return it as a float."""

    return struct.unpack("!f", struct.pack("!f", value))[0]


def solve_binary32(case: SensorCase) -> tuple[float, float]:
    """Solve the stored binary32 system with rounding after each operation."""

    one = binary32(1.0)
    stored_y1 = binary32(case.y1)
    stored_y2 = binary32(case.y2)
    stored_coefficient = binary32(1.0 + case.separation)
    stored_separation = binary32(stored_coefficient - one)
    if stored_separation == 0.0:
        raise ValueError("sensor separation is zero after binary32 storage")

    difference = binary32(stored_y2 - stored_y1)
    c_b = binary32(difference / stored_separation)
    c_a = binary32(stored_y1 - c_b)
    return c_a, c_b


def solve_binary64(case: SensorCase) -> tuple[float, float]:
    """Solve the nominal system using Python's binary64 arithmetic."""

    if case.separation == 0.0:
        raise ValueError("sensor separation must be nonzero")
    c_b = (case.y2 - case.y1) / case.separation
    c_a = case.y1 - c_b
    return c_a, c_b


def decimal_reference(case: SensorCase) -> tuple[Decimal, Decimal]:
    """Solve the declared decimal inputs with 50-digit Decimal arithmetic."""

    with localcontext() as context:
        context.prec = 50
        y1 = Decimal(str(case.y1))
        y2 = Decimal(str(case.y2))
        separation = Decimal(str(case.separation))
        if separation == 0:
            raise ValueError("sensor separation must be nonzero")
        c_b = (y2 - y1) / separation
        c_a = y1 - c_b
    return c_a, c_b


def residual_inf_norm(
    case: SensorCase, concentrations: tuple[float, float]
) -> float:
    """Return the maximum absolute residual in normalized response units."""

    c_a, c_b = concentrations
    residual_1 = c_a + c_b - case.y1
    residual_2 = c_a + (1.0 + case.separation) * c_b - case.y2
    return max(abs(residual_1), abs(residual_2))


def condition_number_2(separation: float) -> float:
    """Return the matrix 2-norm condition number without a small subtraction."""

    if separation == 0.0:
        return math.inf

    # For A = [[1, 1], [1, 1 + d]], det(A)^2 = d^2.  Compute the
    # larger eigenvalue of A.T A directly, then use the eigenvalue product
    # instead of obtaining the smaller eigenvalue by cancellation.
    trace = 4.0 + 2.0 * separation + separation * separation
    discriminant = math.sqrt(trace * trace - 4.0 * separation * separation)
    lambda_max = 0.5 * (trace + discriminant)
    return lambda_max / abs(separation)


def concentration_envelope(case: SensorCase) -> ConcentrationEnvelope:
    """Propagate deterministic reading bounds by evaluating all four corners."""

    with localcontext() as context:
        context.prec = 50
        y1_nominal = Decimal(str(case.y1))
        y2_nominal = Decimal(str(case.y2))
        separation = Decimal(str(case.separation))
        bound = Decimal(str(case.reading_bound))
        if separation == 0:
            raise ValueError("sensor separation must be nonzero")

        concentrations: list[tuple[Decimal, Decimal]] = []
        for y1 in (y1_nominal - bound, y1_nominal + bound):
            for y2 in (y2_nominal - bound, y2_nominal + bound):
                c_b = (y2 - y1) / separation
                c_a = y1 - c_b
                concentrations.append((c_a, c_b))

    c_a_values = [pair[0] for pair in concentrations]
    c_b_values = [pair[1] for pair in concentrations]
    total_values = [c_a + c_b for c_a, c_b in concentrations]
    return ConcentrationEnvelope(
        c_a_min=float(min(c_a_values)),
        c_a_max=float(max(c_a_values)),
        c_b_min=float(min(c_b_values)),
        c_b_max=float(max(c_b_values)),
        total_min=float(min(total_values)),
        total_max=float(max(total_values)),
    )


def classify_value(c_a: float, threshold: float) -> str:
    """Classify a nominal value for the strict c_A > threshold question."""

    return "yes" if c_a > threshold else "no"


def classify_interval(lower: float, upper: float, threshold: float) -> str:
    """Classify a strict threshold over a deterministic admissible interval."""

    if lower > threshold:
        return "yes"
    if upper <= threshold:
        return "no"
    return "indeterminate"


def build_evidence_record(case: SensorCase) -> dict[str, object]:
    """Assemble the evidence needed for the decision-facing statement."""

    binary32_solution = solve_binary32(case)
    binary64_solution = solve_binary64(case)
    reference = decimal_reference(case)
    envelope = concentration_envelope(case)
    reference_float = (float(reference[0]), float(reference[1]))

    return {
        "claim": (
            "decide whether c_A is strictly greater than "
            f"{case.threshold_mg_per_l} mg/L"
        ),
        "case": asdict(case),
        "units": {
            "concentrations": "mg/L",
            "readings": "normalized response units",
        },
        "reference": {
            "kind": "50-digit Decimal solution of the declared decimal inputs",
            "c_a_mg_per_l": str(reference[0]),
            "c_b_mg_per_l": str(reference[1]),
        },
        "precision_variation": {
            "binary32": {
                "c_a_mg_per_l": binary32_solution[0],
                "c_b_mg_per_l": binary32_solution[1],
                "nominal_decision": classify_value(
                    binary32_solution[0], case.threshold_mg_per_l
                ),
                "residual_inf_norm_response_units": residual_inf_norm(
                    case, binary32_solution
                ),
            },
            "binary64": {
                "c_a_mg_per_l": binary64_solution[0],
                "c_b_mg_per_l": binary64_solution[1],
                "nominal_decision": classify_value(
                    binary64_solution[0], case.threshold_mg_per_l
                ),
                "forward_error_inf_norm_mg_per_l": max(
                    abs(binary64_solution[index] - reference_float[index])
                    for index in (0, 1)
                ),
                "residual_inf_norm_response_units": residual_inf_norm(
                    case, binary64_solution
                ),
            },
        },
        "conditioning": {
            "matrix_2_norm_condition_number": condition_number_2(
                case.separation
            )
        },
        "deterministic_input_envelope": asdict(envelope),
        "supported_decision": classify_interval(
            envelope.c_a_min,
            envelope.c_a_max,
            case.threshold_mg_per_l,
        ),
        "limitations": [
            "the deterministic reading bounds are not probabilities",
            "the linear sensor model and calibration are assumed, not validated",
            "only the emulated binary32 and current Python binary64 paths were tested",
        ],
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
    }


def reliability_statement(case: SensorCase) -> str:
    """Return a concise statement supported by the assembled evidence."""

    c_a_64, _ = solve_binary64(case)
    c_a_reference, _ = decimal_reference(case)
    envelope = concentration_envelope(case)
    condition = condition_number_2(case.separation)
    binary64_error = abs(c_a_64 - float(c_a_reference))
    status = classify_interval(
        envelope.c_a_min, envelope.c_a_max, case.threshold_mg_per_l
    )

    return (
        "Under the declared linear two-sensor model, the binary64 nominal "
        f"estimate is c_A = {c_a_64:.3f} mg/L and agrees with the exact-decimal "
        f"nominal reference to {binary64_error:.2e} mg/L. However, the matrix "
        f"2-norm condition number is approximately {condition:.2e}, and the "
        "deterministic sensor-reading bounds imply "
        f"c_A in [{envelope.c_a_min:.2f}, {envelope.c_a_max:.2f}] mg/L, "
        f"which crosses the strict {case.threshold_mg_per_l:.2f} mg/L threshold; "
        f"the supported decision is therefore {status}. The total concentration "
        f"remains in [{envelope.total_min:.8f}, {envelope.total_max:.8f}] mg/L. "
        "This evidence does not validate the linear sensor model, assign a "
        "probability to the input bounds, or establish behaviour on untested "
        "precision and hardware paths."
    )


def print_baseline(case: SensorCase) -> None:
    """Print the suspicious supplied result without revealing the diagnosis."""

    binary32_solution = solve_binary32(case)
    print("scientific question: is c_A > 0.61 mg/L?")
    print(f"required absolute accuracy: {case.required_accuracy_mg_per_l:.2f} mg/L")
    print("stored precision: binary32")
    print(f"c_A: {binary32_solution[0]:.9f} mg/L")
    print(f"c_B: {binary32_solution[1]:.9f} mg/L")
    print(f"decision: {classify_value(binary32_solution[0], case.threshold_mg_per_l)}")
    print(
        "residual infinity norm: "
        f"{residual_inf_norm(case, binary32_solution):.3e} response units"
    )


def print_report(case: SensorCase) -> None:
    """Print the complete reference evidence record and conclusion."""

    print(json.dumps(build_evidence_record(case), indent=2, sort_keys=True))
    print("\nqualified reliability statement\n")
    print(reliability_statement(case))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        action="store_true",
        help="print the complete evidence record instead of only the baseline",
    )
    arguments = parser.parse_args()
    case = SensorCase()
    if arguments.report:
        print_report(case)
    else:
        print_baseline(case)


if __name__ == "__main__":
    main()
