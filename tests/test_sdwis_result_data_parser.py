from unittest import TestCase

from sdwis_drink_water.data_praser import ResultDataParser
from mock_data import pb90_exceed_past_rule, pb90_exceed_new_rule


class SdwisResultDataParserTests(TestCase):
    pb90_exceed_past_rule_data_parse = ResultDataParser(pb90_exceed_past_rule)
    pb90_exceed_new_rule_data_parse = ResultDataParser(pb90_exceed_new_rule)

    def test_intersect_with(self):
        result_number = self.pb90_exceed_past_rule_data_parse.intersect_with(
            self.pb90_exceed_new_rule_data_parse).count()
        self.assertEqual(result_number, min(len(self.pb90_exceed_past_rule_data_parse.data),
                                            len(self.pb90_exceed_new_rule_data_parse.data)))

    def test_merge_with(self):
        result_number = self.pb90_exceed_past_rule_data_parse.merge_with(self.pb90_exceed_new_rule_data_parse).count()
        self.assertEqual(result_number, max(len(self.pb90_exceed_past_rule_data_parse.data),
                                            len(self.pb90_exceed_new_rule_data_parse.data)))

    def test_difference_with(self):
        result_number_small_difference_large = self.pb90_exceed_past_rule_data_parse.difference_with(
            self.pb90_exceed_new_rule_data_parse).count()
        result_number_large_difference_small = self.pb90_exceed_new_rule_data_parse.difference_with(
            self.pb90_exceed_past_rule_data_parse).count()

        self.assertEqual(result_number_small_difference_large, 0)
        self.assertEqual(result_number_large_difference_small,
                         len(self.pb90_exceed_new_rule_data_parse.data) - len(
                             self.pb90_exceed_past_rule_data_parse.data), )
