from sdwis_drink_water import WaterSystem

water_system_api = WaterSystem(print_url=True)

# fetch first data from WaterSystem table
water_system_api.get_table_first_data()

# fetch columns descriptions of WaterSystem table
water_system_api.get_table_columns_description()

# fetch first n data from WaterSystem table
water_system_api.get_table_first_n_data(n=2, print_to_console=True)

# get summarize data number according to epa_region
water_system_api.summarize_water_system_data_by_epa_region(multi_threads=True, print_to_console=True)

# get data according to epa_region
water_system_api_epa_1 = water_system_api.get_water_system_by_epa_region(epa_region=1, print_to_console=True)
# export data to xlsx
water_system_api_epa_1.export_data("./output_files/water_system_epa_1.xlsx", format_type="xlsx")
# print all keys to determine how to use this data
print(water_system_api_epa_1.get_all_keys())

