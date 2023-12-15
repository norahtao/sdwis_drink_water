from sdwis_drink_water import WaterSystem

water_system_api = WaterSystem(print_url=True)

# fetch first data from Water_System table
water_system_api.get_table_first_data()

# fetch first n data from Water_System table
water_system_api.get_table_first_n_data(n=2, print_to_console=True)

# get summarize data number according to epa_region
water_system_api.summarize_water_system_data_by_epa_region(multi_threads=True, print_to_console=True)

water_system_epa_1 = water_system_api.get_water_system_by_epa_region(epa_region=1, print_to_console=True)
# export data to xlsx
water_system_epa_1.export_data("./output_files/water_system_epa_1.xlsx", format_type="xlsx")
# print all keys to determine how to use this data
print(water_system_epa_1.get_all_keys())

# find by condition "is_grant_eligible_ind==Y"
is_grant_eligible_ind = water_system_epa_1.find_by_condition("is_grant_eligible_ind=Y")
print(is_grant_eligible_ind.count())

# find by condition "is_wholesaler_ind==Y"
is_wholesaler_ind = water_system_epa_1.find_by_condition("is_wholesaler_ind=Y")
print(is_wholesaler_ind.count())

# find by condition "is_grant_eligible_ind==Y" and "is_wholesaler_ind==Y"
is_grant_eligible_ind_and_is_wholesaler_ind = is_grant_eligible_ind.find_by_condition("is_wholesaler_ind=Y")
print(is_grant_eligible_ind_and_is_wholesaler_ind.count())
is_grant_eligible_ind_and_is_wholesaler_ind.show()

# export data to csv
is_grant_eligible_ind_and_is_wholesaler_ind.export_data("./output_files/water_system_epa_1_filtered_result.csv",
                                                        format_type="csv")
