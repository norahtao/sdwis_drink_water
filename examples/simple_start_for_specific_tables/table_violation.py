from sdwis_drink_water import Violation

violation_api = Violation(print_url=True)

# fetch first data from Violation table
violation_api.get_table_first_data()

# fetch columns descriptions of Violation table
violation_api.get_table_columns_description()

# fetch first n data from Violation table
violation_api.get_table_first_n_data(n=2, print_to_console=True)

# get summarize data number according to epa_region
violation_api.summarize_violation_data_by_epa_region(multi_threads=True, print_to_console=True)

violation_api_epa_1 = violation_api.get_violation_by_epa_region(epa_region=1, print_to_console=True)
# export data to xlsx
violation_api_epa_1.export_data("./output_files/violation_epa_1.xlsx", format_type="xlsx")
# print all keys to determine how to use this data
print(violation_api_epa_1.get_all_keys())

