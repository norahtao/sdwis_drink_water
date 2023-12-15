
from sdwis_drink_water import SdwisTable

class Treatment:
    def __init__(self, print_url=False):
        self.sdwis_table = SdwisTable(print_url=print_url)
        self.TABLE_NAME = "TREATMENT"
    
    def get_table_column_name(self, print_to_console=True):
        return self.sdwis_table.get_table_column_name_by_table_name(table_name=self.TABLE_NAME,
                                                                    print_to_console=print_to_console)
    
    def get_table_columns_description(self, multi_threads=False, print_to_console=True):
        return self.sdwis_table.get_columns_description_by_table_name(table_name=self.TABLE_NAME,
                                                                    print_to_console=print_to_console, 
                                                                    multi_threads=multi_threads)                                                       
    def get_table_data_number(self):
        return self.sdwis_table.get_table_data_number(table_name=self.TABLE_NAME)
        
    def get_table_first_data(self, print_to_console=True):
        return self.sdwis_table.get_table_first_data_by_table_name(table_name=self.TABLE_NAME,
                                                                   print_to_console=print_to_console)

    def get_table_first_n_data(self, n=0, multi_threads=False, print_to_console=True):
        return self.sdwis_table.get_table_first_n_data_by_table_name(table_name=self.TABLE_NAME, n=n,
                                                                     multi_threads=multi_threads, print_to_console=print_to_console)                                                              

    def get_treatment_data_by_conditions(self, condition1="", condition2="", condition3="", print_to_console=True,
                                          only_count=False):
        return self.sdwis_table.get_data_by_conditions(table_name=self.TABLE_NAME, condition1=condition1,
                                                condition2=condition2, condition3=condition3,
                                                print_to_console=print_to_console, only_count=only_count)
