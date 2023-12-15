# BACKGROUND: EPA is proposing to lower the lead action level from 15 µg/L (0.015mg/L) to 10 µg/L (0.01mg/L)
# We want to look at the database and see those samples that match the original rule, but not the new one.
from sdwis_drink_water import LcrSampleResult

lcr_sample_result_api = LcrSampleResult(print_url=True)

# fetch first data from LcrSampleResult table
lcr_sample_result_api.get_table_first_data()
# Setting "multi_threads=True" will use multithreading to speed up the fetching of data
lcr_sample_result_api.get_table_columns_description(multi_threads=True)

# Samples exceeding the original rule
pb90_exceed_original_rule = lcr_sample_result_api.get_lcr_sample_result_data_by_conditions("contaminant_code=PB90",
                                                                                           "result_sign_code==",
                                                                                           "sample_measure>0.015")
# Samples exceeding the new rule
pb90_exceed_new_rule = lcr_sample_result_api.get_lcr_sample_result_data_by_conditions("contaminant_code=PB90",
                                                                                      "result_sign_code==",
                                                                                      "sample_measure>0.01")
# fetch their intersection, union, difference
# here intersection is the number of pb90_exceed_original_rule
print(pb90_exceed_original_rule.intersect_with(pb90_exceed_new_rule).count())
# here union is the number of pb90_exceed_new_rule
print(pb90_exceed_original_rule.merge_with(pb90_exceed_new_rule).count())
# get difference. These samples comply with the original rule, but not the new rule. Additional attention is required
print(pb90_exceed_new_rule.difference_with(pb90_exceed_original_rule).count())

result_we_need = pb90_exceed_new_rule.difference_with(pb90_exceed_original_rule)
result_we_need.export_data("./output_files/Sample sets for additional attention in the new regulation of Lead.xlsx",
                           format_type="xlsx")
