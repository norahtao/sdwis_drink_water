from sdwis_drink_water import GeographicArea

geographic_area_api = GeographicArea(print_url=True)

# fetch first data from GeographicArea table
geographic_area_api.get_table_first_data()

# fetch columns descriptions of GeographicArea table
geographic_area_api.get_table_columns_description()

# fetch first n data from GeographicArea table
geographic_area_api.get_table_first_n_data(n=2, print_to_console=True)

# get summarize data number according to epa_region
geographic_area_api.summarize_geographic_area_data_by_epa_region(multi_threads=True, print_to_console=True)

geographic_area_api_epa_1 = geographic_area_api.get_geographic_area_by_epa_region(epa_region=1, print_to_console=True)
# export data to xlsx
geographic_area_api_epa_1.export_data("./output_files/geographic_area_epa_1.xlsx", format_type="xlsx")
# print all keys to determine how to use this data
print(geographic_area_api_epa_1.get_all_keys())

