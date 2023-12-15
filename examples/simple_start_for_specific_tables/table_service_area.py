from sdwis_drink_water import ServiceArea

service_area_api = ServiceArea(print_url=True)

# fetch first data from ServiceArea table
service_area_api.get_table_first_data()

# fetch columns descriptions of ServiceArea table
service_area_api.get_table_columns_description()

# fetch first n data from ServiceArea table
service_area_api.get_table_first_n_data(n=2, print_to_console=True)
