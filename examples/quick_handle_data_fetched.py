from sdwis_drink_water import SdwisTable

# "print_url=True" here will cause subsequent queries to display the requested URL
table_api = SdwisTable(print_url=True)
# fetch first 1000 data from LCR_SAMPLE_RESULT table
result = table_api.get_table_first_n_data_by_table_name(table_name="LCR_SAMPLE_RESULT", n=1000, print_to_console=False)
# get all keys of result data
print(result.get_all_keys())

# get first n data in results
first_one = result.get_first_n_records(1)
first_one.show()

print("find max sample_measure in results")
max_one = result.find_max("sample_measure")
max_one.show()

print("find max sample_measure in results with condition (contaminant_code==PB90)")
max_one_limited_to_pb = result.find_max_with_condition("sample_measure", condition="contaminant_code==PB90")
max_one_limited_to_pb.show()

# export data to a specific file
result.export_data("output.xlsx", format_type="xlsx")
# result.export_data("output.parquet", format_type="parquet")
# result.export_data("output.csv", format_type="csv")
# result.export_data("output.txt", format_type="txt")
