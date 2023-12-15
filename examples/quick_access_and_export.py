from sdwis_drink_water import LcrSampleResult

lcr_sample_result_api = LcrSampleResult(print_url=True)

all_lcr_sample = lcr_sample_result_api.get_table_first_n_data(n=99999999, multi_threads=True, print_to_console=False)
all_lcr_sample.export_data("all_lcr_samples.xlsx", format_type="xlsx")
