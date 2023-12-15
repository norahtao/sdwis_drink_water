from unittest import TestCase

from sdwis_drink_water.configs import TABLES_LIST
from sdwis_drink_water import SdwisAPI, SdwisTable


class SdwisTableTests(TestCase):
    def setUp(self):
        self.api = SdwisAPI(enable_cache=False)
        self.table_api = SdwisTable()

    def test_get_all_table_names(self):
        self.table_api.get_all_table_names(print_to_console=True)
        data = self.table_api.get_all_table_names(print_to_console=False)
        self.assertEqual(data, TABLES_LIST)

    def test_get_all_table_names_and_descriptions(self):
        self.table_api.get_all_table_names_and_descriptions(print_to_console=True)
        data = self.table_api.get_all_table_names_and_descriptions(print_to_console=False)
        expected_dict = {
            "ENFORCEMENT_ACTION": "Documents actions taken against a Public Water System (PWS), laboratory, or operator. Includes requirements that must be met in order to rectify a failure to perform under the Public Water Supply Supervision (PWSS) Program. Enforcement actions are informal and formal. They may be issued by the Primacy State (or its representative) or the EPA. Examples: administrative and civil/criminal legal actions, warning notices, citations, orders to follow water treatment procedures, orders to follow sampling requirements, orders to resolve violations, moratoriums on connections, temporary injunctions, restraining orders, penalties, and orders to comply with reporting requirements. Example descriptors: type of enforcement action, directed actions, and milestone date(s).",
            "GEOGRAPHIC_AREA": "Information on political units established by geographic boundaries, such as state, town, or county served by a Water System.",
            "LCR_SAMPLE_RESULT": "90th percentile sample summary results data for lead or copper.",
            "LCR_SAMPLE": "90th percentile sample summaries data for lead or copper.",
            "SERVICE_AREA": "A service area defines the sensitive populations that receive water from the water system.",
            "TREATMENT": "Treatment objectives and process for treating water from a water system facility.",
            "WATER_SYSTEM": "Inventory information on public water systems.",
            "WATER_SYSTEM_FACILITY": "Inventory information on public water system facilities.",
            "VIOLATION": "Documents a breach of a requirement. Violations are detected by assessment of sample results or reviews (including on site visits). Violations may lead to legal actions or compliance orders. Violations are publicized, when required, by public notification. Violations may be remedied by compliance/enforcement remedies, such as improved filtration techniques or changes in procedures. Examples: Maximum Contaminant Level (MCL) violations, failure to replace lead service lines, monitoring and reporting violations, treatment technique violations, and procedural violations. Example descriptors: type, date, description, severity, and recommended corrective action(s) to include milestones.",
            "VIOLATION_ENF_ASSOC": "Association between a violation and an enforcement action."
        }
        self.assertEqual(data, expected_dict)
