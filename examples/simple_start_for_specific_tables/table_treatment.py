from sdwis_drink_water import Treatment

treatment_api = Treatment(print_url=True)

# fetch first data from Treatment table
treatment_api.get_table_first_data()

# fetch columns descriptions of Treatment table
treatment_api.get_table_columns_description()

# fetch first n data from Treatment table
treatment_api.get_table_first_n_data(n=2, print_to_console=True)
