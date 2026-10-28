import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from triunfo.evaluation import parse_single_call, score_call


class CallEvaluationTests(unittest.TestCase):
    tools = [{"name": "Get Sunrise and Sunset Times"}, {"name": "f"}]
    reference = '[Get Sunrise and Sunset Times(string="2024-05-14", latitude=37.7749, longitude=-122.4194)]'

    def test_reads_names_with_spaces_and_literal_arguments(self):
        self.assertEqual(parse_single_call(self.reference, self.tools), {
            "name": "Get Sunrise and Sunset Times",
            "arguments": {"string": "2024-05-14", "latitude": 37.7749, "longitude": -122.4194},
        })

    def test_rejects_positional_value_after_keyword_from_pilot(self):
        prediction = '[Get Sunrise and Sunset Times(latitude=37.7689,-122.4052,string="today",timezone="America/Los_Angeles")]'
        self.assertEqual(score_call(prediction, self.reference, self.tools), {
            "parseable_call": False, "tool_correct": False, "call_exact": False,
        })

    def test_rejects_multiple_calls_for_single_call_protocol(self):
        self.assertIsNone(parse_single_call('[f(x=1), f(x=2)]', self.tools))

    def test_rejects_expressions_instead_of_literal_values(self):
        self.assertIsNone(parse_single_call('[f(x=1 + 2)]', self.tools))

    def test_rejects_repeated_argument_instead_of_overwriting(self):
        self.assertIsNone(parse_single_call('[f(x=1, x=2)]', self.tools))

    def test_argument_order_does_not_change_exact_match(self):
        self.assertEqual(score_call('[f(y="a", x=2)]', '[f(x=2, y="a")]', self.tools), {
            "parseable_call": True, "tool_correct": True, "call_exact": True,
        })

    def test_extra_argument_is_not_exact_reference_match(self):
        self.assertEqual(score_call('[f(x=2, y=3)]', '[f(x=2)]', self.tools), {
            "parseable_call": True, "tool_correct": True, "call_exact": False,
        })

    def test_boolean_is_not_scored_as_numeric_one(self):
        self.assertEqual(score_call('[f(x=True)]', '[f(x=1)]', self.tools), {
            "parseable_call": True, "tool_correct": True, "call_exact": False,
        })

    def test_unsupported_reference_is_reported_instead_of_scored(self):
        with self.assertRaises(ValueError):
            score_call('[f(x=1)]', 'Please provide a value.', self.tools)


if __name__ == "__main__":
    unittest.main()
