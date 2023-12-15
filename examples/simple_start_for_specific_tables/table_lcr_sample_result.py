from sdwis_drink_water import LcrSampleResult

lcr_sample_result_api = LcrSampleResult(print_url=True)

# fetch first data from LcrSampleResult table
lcr_sample_result_api.get_table_first_data()

# fetch columns descriptions of LcrSampleResult table
lcr_sample_result_api.get_table_columns_description()

# fetch first n data from LcrSampleResult table
lcr_sample_result_api.get_table_first_n_data(n=2, print_to_console=True)

# get summarize data number according to epa_region
lcr_sample_result_api.summarize_lcr_sample_result_data_by_epa_region(multi_threads=True, print_to_console=True)

lcr_sample_result_api_epa_1 = lcr_sample_result_api.get_lcr_sample_result_by_epa_region(epa_region=1, print_to_console=True)
# export data to xlsx
lcr_sample_result_api_epa_1.export_data("./output_files/lcr_sample_result_epa_1.xlsx", format_type="xlsx")
# print all keys to determine how to use this data
print(lcr_sample_result_api_epa_1.get_all_keys())

