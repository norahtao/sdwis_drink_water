from sdwis_drink_water import EnforcementAction

enforcement_action_api = EnforcementAction(print_url=True)

# fetch first data from EnforcementAction table
enforcement_action_api.get_table_first_data()

# fetch columns descriptions of EnforcementAction table
enforcement_action_api.get_table_columns_description()

# fetch first n data from EnforcementAction table
enforcement_action_api.get_table_first_n_data(n=2, print_to_console=True)
