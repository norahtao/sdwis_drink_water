from sdwis_drink_water import SdwisTable

# "print_url=True" here will cause subsequent queries to display the requested URL
table_api = SdwisTable(print_url=False)
# "print_to_console=True" here causes all subsequent queries to be printed

# fetch all table names
table_names = table_api.get_all_table_names(print_to_console=True)
# fetch all table names with description (Crawl the latest information from the website)
table_api.get_all_table_names_and_descriptions(print_to_console=True)

# fetch structure for specific table name
for table_name in table_names:
    print(f"======{table_names}======")
    table_api.get_table_column_name_by_table_name(table_name=table_name, print_to_console=True)
# fetch first data for specific table name
for table_name in table_names:
    print(f"======{table_names}======")
    table_api.get_table_first_data_by_table_name(table_name=table_name, print_to_console=True)
# fetch first n for specific table name
for table_name in table_names:
    print(f"======{table_names}======")
    table_api.get_table_first_n_data_by_table_name(table_name=table_name, n=1, print_to_console=True)
