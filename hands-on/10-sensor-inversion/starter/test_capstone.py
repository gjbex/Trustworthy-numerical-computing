"""Verification checks for the Module 10 sensor-inversion capstone."""

import math
import unittest
from decimal import Decimal

from capstone import (
    SensorCase,
    build_evidence_record,
    classify_interval,
    condition_number_2,
    concentration_envelope,
    decimal_reference,
    reliability_statement,
    residual_inf_norm,
    solve_binary32,
    solve_binary64,
)


class SensorInversionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.case = SensorCase()

    def test_supplied_binary32_baseline(self) -> None:
        concentrations = solve_binary32(self.case)
        self.assertEqual(concentrations, (0.625, 0.375))
        self.assertLess(residual_inf_norm(self.case, concentrations), 3.0e-8)
        self.assertGreater(concentrations[0], self.case.threshold_mg_per_l)

    def test_binary32_rejects_unrepresentable_sensor_separation(self) -> None:
        case = SensorCase(y2=1.000000004, separation=1.0e-8)
        with self.assertRaisesRegex(ValueError, "zero after binary32 storage"):
            solve_binary32(case)

    def test_decimal_reference_is_exact_for_declared_inputs(self) -> None:
        c_a, c_b = decimal_reference(self.case)
        self.assertEqual(c_a, Decimal("0.6"))
        self.assertEqual(c_b, Decimal("0.4"))

    def test_binary64_nominal_solution_meets_accuracy_requirement(self) -> None:
        reference = tuple(float(value) for value in decimal_reference(self.case))
        observed = solve_binary64(self.case)
        forward_error = max(
            abs(observed[index] - reference[index]) for index in (0, 1)
        )
        self.assertLess(forward_error, self.case.required_accuracy_mg_per_l)
        self.assertLess(forward_error, 2.0e-11)
        self.assertLessEqual(observed[0], self.case.threshold_mg_per_l)

    def test_condition_number_exposes_sensitivity(self) -> None:
        observed = condition_number_2(self.case.separation)
        self.assertTrue(math.isclose(observed, 4_000_002.0, rel_tol=1.0e-12))

    def test_well_separated_control_is_accurate_in_binary32(self) -> None:
        control = SensorCase(y2=1.04, separation=0.1)
        c_a, c_b = solve_binary32(control)
        self.assertLess(abs(c_a - 0.6), 1.0e-5)
        self.assertLess(abs(c_b - 0.4), 1.0e-5)
        self.assertLess(condition_number_2(control.separation), 50.0)

    def test_deterministic_input_envelope_crosses_threshold(self) -> None:
        envelope = concentration_envelope(self.case)
        self.assertTrue(
            math.isclose(envelope.c_a_min, 0.49999995, abs_tol=1.0e-15)
        )
        self.assertTrue(
            math.isclose(envelope.c_a_max, 0.70000005, abs_tol=1.0e-15)
        )
        self.assertEqual(
            classify_interval(
                envelope.c_a_min,
                envelope.c_a_max,
                self.case.threshold_mg_per_l,
            ),
            "indeterminate",
        )
        self.assertLess(envelope.total_max - envelope.total_min, 2.0e-7)

    def test_interval_classification_handles_all_outcomes(self) -> None:
        self.assertEqual(classify_interval(0.7, 0.8, 0.61), "yes")
        self.assertEqual(classify_interval(0.5, 0.6, 0.61), "no")
        self.assertEqual(classify_interval(0.5, 0.7, 0.61), "indeterminate")

    def test_evidence_record_keeps_claims_separate(self) -> None:
        record = build_evidence_record(self.case)
        self.assertEqual(record["supported_decision"], "indeterminate")
        self.assertIn("reference", record)
        self.assertIn("conditioning", record)
        self.assertIn("deterministic_input_envelope", record)
        self.assertGreaterEqual(len(record["limitations"]), 3)

    def test_reliability_statement_is_qualified(self) -> None:
        statement = reliability_statement(self.case).lower()
        for required_text in (
            "mg/l",
            "condition",
            "indeterminate",
            "does not validate",
            "deterministic",
        ):
            with self.subTest(required_text=required_text):
                self.assertIn(required_text, statement)


if __name__ == "__main__":
    unittest.main()
