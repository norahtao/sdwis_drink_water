from sdwis_drink_water import ViolationEnfAssoc

violation_enf_assoc_api = ViolationEnfAssoc(print_url=True)

# fetch first data from ViolationEnfAssoc table
violation_enf_assoc_api.get_table_first_data()

# fetch columns descriptions of ViolationEnfAssoc table
violation_enf_assoc_api.get_table_columns_description()

# fetch first n data from ViolationEnfAssoc table
violation_enf_assoc_api.get_table_first_n_data(n=2, print_to_console=True)
