import threading
import time

from tqdm import tqdm
import logging
import tabulate

from sdwis_drink_water import SdwisAPI
from sdwis_drink_water.configs import TABLES_LIST, EPA_REGION_ID, MAX_QUERY_DATA_LIMIT_A_TIME
from sdwis_drink_water.data_praser import ResultDataParser
from sdwis_drink_water.errors import SdwisQueryParamsException
from sdwis_drink_water.utils import get_table_description, _is_epa_region_param_valid, _is_table_has_epa_region, \
    process_table_column_condition, print_tabulate_result_with_divider, get_column_description

log = logging.getLogger(__name__)


class SdwisTable:
    def __init__(self, enable_cache=True, print_url=False):
        self.sdwis_api = SdwisAPI(enable_cache=enable_cache, print_url=print_url)

    def _get_data_by_request(self, query_url, print_to_console=False, multi_threads=False):
        query_result = self.sdwis_api.get_request(query_url, multi_mode=multi_threads)
        if print_to_console:
            headers = query_result[0].keys()
            values = [list(record.values()) for record in query_result]
            # tabulate_result = tabulate.tabulate(values, headers=headers)
            # print_tabulate_result_with_divider(tabulate_result)
            table = tabulate.tabulate(values, headers, tablefmt="simple_grid")
            print(table)
        return query_result

    def _get_result_data_by_request(self, query_url, print_to_console=False):
        query_result = self.sdwis_api.get_request(query_url)
        if print_to_console:
            headers = query_result[0].keys()
            values = [list(record.values()) for record in query_result]
            tabulate_result = tabulate.tabulate(values, headers=headers, tablefmt="simple_grid")
            print_tabulate_result_with_divider(tabulate_result)
        return ResultDataParser(query_result)

    def get_all_table_names(self, print_to_console=True):
        """

        :param print_to_console:
        :param kwargs:
        :return:
        """
        if print_to_console:
            header = ["table_name"]
            tabulate_result = tabulate.tabulate([[i] for i in TABLES_LIST], headers=header)
            print_tabulate_result_with_divider(tabulate_result)
            return TABLES_LIST
        else:
            return TABLES_LIST

    def get_all_table_names_and_descriptions(self, print_to_console=True):
        table_descriptions = []
        for table_name in tqdm(TABLES_LIST, desc='Fetching table descriptions from SDWIS Official Website'):
            description = get_table_description(table_name, session=self.sdwis_api.multi_threads_session)
            table_descriptions.append(description)

        if print_to_console:
            headers = ["table_name", "description"]
            table_name_description_list = [[TABLES_LIST[i], table_descriptions[i]] for i in range(len(TABLES_LIST))]
            tabulate_result = tabulate.tabulate(table_name_description_list, headers=headers, tablefmt="simple_grid")
            print_tabulate_result_with_divider(tabulate_result)
            return tabulate_result
        else:
            return dict(zip(TABLES_LIST, table_descriptions))

    def get_table_column_name_by_table_name(self, table_name="", print_to_console=True):
        first_data = self.get_table_first_data_by_table_name(table_name=table_name, print_to_console=False)
        if print_to_console:
            column_names = list(first_data.get_all_keys())
            print(column_names)
            # headers = [f"COLUMN_{i + 1}" for i in range(len(column_names))]
            # tabulate_result = tabulate.tabulate([column_names], headers=headers, numalign="right", stralign="right")
            # print_tabulate_result_with_divider(tabulate_result)
        return first_data.get_all_keys()

    def get_columns_description_by_table_name(self, table_name="", print_to_console=True, multi_threads=False):
        first_data = self.get_table_first_data_by_table_name(table_name=table_name, print_to_console=False)
        column_names = list(first_data.get_all_keys())
        column_descriptions = []
        if multi_threads:
            def thread_task(column_name_):
                description_ = get_column_description(column_name_, session=self.sdwis_api.multi_threads_session)
                column_descriptions.append(description_)
                pbar.update(1)

            pbar = tqdm(total=len(column_names),
                        desc=f"Fetching column descriptions for {table_name} from SDWIS Official Website by multi_threads_mode")
            threads = []
            for column_name in column_names:
                thread = threading.Thread(target=thread_task, args=(column_name,))
                threads.append(thread)
                thread.start()
                if len(threads) >= len(column_names):
                    for t in threads:
                        t.join()
                    threads = []
            for t in threads:
                t.join()
            pbar.close()
        else:
            for column_name in tqdm(column_names,
                                    desc=f"Fetching column descriptions for {table_name} from SDWIS Official Website"):
                description = get_column_description(column_name, session=self.sdwis_api.session)
                column_descriptions.append(description)

        if print_to_console:
            headers = ["column_names", "description"]
            table_column_description_list = [[column_names[i], column_descriptions[i]] for i in
                                             range(len(column_names))]
            tabulate_result = tabulate.tabulate(table_column_description_list, headers=headers, tablefmt="simple_grid")
            print_tabulate_result_with_divider(tabulate_result)
        return dict(zip(column_names, column_descriptions))

    def get_table_data_number(self, table_name=""):
        total_data_number = self.get_data_by_conditions(table_name=table_name, print_to_console=False, only_count=True)
        return total_data_number

    def get_table_first_data_by_table_name(self, table_name="", print_to_console=True):
        return self.get_table_first_n_data_by_table_name(table_name=table_name, print_to_console=print_to_console, n=1)

    def get_table_first_n_data_by_table_name(self, table_name="", n=0, print_to_console=True, multi_threads=False):
        # Handle requests exceeding the maximum limit, should divide to several request
        if n > MAX_QUERY_DATA_LIMIT_A_TIME:
            query_result = []
            print(table_name)
            total_data = self.get_data_by_conditions(table_name=table_name, print_to_console=False, only_count=True)
            if n >= total_data:
                print(
                    f"The data number in the database provided by the API is {total_data}. Your request number exceeds this limit, please note.")
                n = total_data - 1

            # Calculate the number of full batches and the remainder for the last batch
            num_full_batches = n // MAX_QUERY_DATA_LIMIT_A_TIME
            remainder = n % MAX_QUERY_DATA_LIMIT_A_TIME
            batches = []
            for i in range(num_full_batches):
                start = i * MAX_QUERY_DATA_LIMIT_A_TIME
                end = (i + 1) * MAX_QUERY_DATA_LIMIT_A_TIME - 1
                batches.append([start, end])
            # Handling the last batch if there's a remainder
            if remainder != 0:
                start = num_full_batches * MAX_QUERY_DATA_LIMIT_A_TIME
                end = n - 1
                batches.append([start, end])
            if multi_threads:
                def thread_task(start_row, end_row):
                    query_url = f"{self.sdwis_api.base_url}/{table_name}/rows/{start_row}:{end_row}"
                    partial_query_result = self._get_data_by_request(query_url,
                                                                     print_to_console=print_to_console,
                                                                     multi_threads=True)
                    query_result.extend(partial_query_result)

                pbar = tqdm(total=len(batches),
                            desc=f"Fetching Data by multi_threads_mode")
                threads = []
                for i in tqdm(range(len(batches))):
                    start_row = batches[i][0]
                    end_row = batches[i][1]
                    thread = threading.Thread(target=thread_task, args=(start_row, end_row))
                    threads.append(thread)
                    if i > 10:
                        time.sleep(2)
                    thread.start()
                    if len(threads) >= len(batches):
                        for t in threads:
                            t.join()
                        threads = []
                for t in threads:
                    t.join()
                pbar.close()
            else:
                # Output the batches
                for i in tqdm(range(len(batches)), desc="Fetching Data"):
                    start_row = batches[i][0]
                    end_row = batches[i][1]
                    query_url = f"{self.sdwis_api.base_url}/{table_name}/rows/{start_row}:{end_row}"
                    partial_query_result = self._get_data_by_request(query_url, print_to_console=print_to_console)
                    query_result.extend(partial_query_result)
        else:
            query_url = f"{self.sdwis_api.base_url}/{table_name}/rows/0:{n - 1}"
            query_result = self._get_data_by_request(query_url, print_to_console=print_to_console)
        return ResultDataParser(query_result)

    def get_data_by_conditions(self, table_name="", condition1="", condition2="", condition3="", print_to_console=True,
                               only_count=False):
        """
        condition_handle is combined with column operation
        :param table_name:
        :param condition1:
        :param condition2:
        :param condition3:
        :param print_to_console:
        :param only_count:
        :param kwargs:
        :return:
        """
        if table_name == "":
            raise SdwisQueryParamsException("table name can't not be empty")
        #  conditions_list contains all the processed conditions
        conditions_url_list = [self.sdwis_api.base_url, table_name]
        conditions_list = []
        # Process each condition_handle if it's not empty
        if condition1 != "":
            conditions_list.append(process_table_column_condition(condition1))
        if condition2 != "":
            conditions_list.append(process_table_column_condition(condition2))
        if condition3 != "":
            conditions_list.append(process_table_column_condition(condition3))

        conditions_url_list = conditions_url_list + conditions_list
        query_url = "/".join(conditions_url_list)
        if only_count:
            total_number = self.sdwis_api.get_request(query_url, only_count=only_count)
            if print_to_console:
                header = ["CONDITION(s)", "DATA_NUMBER_MATCH_CONDITION"]
                tabulate_result = tabulate.tabulate([[" & ".join(conditions_list), total_number]], headers=header,
                                                    tablefmt="simple_grid")
                print_tabulate_result_with_divider(tabulate_result)
            return total_number
        else:
            return self._get_result_data_by_request(query_url)

    def summarize_data_by_epa_region(self, table_name="", print_to_console=True, multi_threads=False):
        """
        :param table_name:
        :param print_to_console:
        :param only_count:
        :param multi_threads:
        :param kwargs:
        :return:
        """
        _is_table_has_epa_region(table_name)
        data_number_list = []

        if multi_threads:
            def thread_task(multi_epa_region_id):
                multi_data_number = self.get_data_by_epa_region(table_name=table_name, epa_region=multi_epa_region_id,
                                                                only_count=True, print_to_console=False,
                                                                multi_mode=multi_threads)
                data_number_list.append(multi_data_number)
                pbar.update(1)

            pbar = tqdm(total=len(EPA_REGION_ID),
                        desc=f"Fetching the total amount of data by EPA region from the {table_name} data table")
            threads = []
            for epa_region_id in EPA_REGION_ID:
                thread = threading.Thread(target=thread_task, args=(epa_region_id,))
                threads.append(thread)
                thread.start()
                if len(threads) >= 10:
                    for t in threads:
                        t.join()
                    threads = []
            for t in threads:
                t.join()
            pbar.close()
        else:
            for epa_region_id in tqdm(EPA_REGION_ID,
                                      desc=F"Fetching the total amount of data by EPA region from the \"{table_name}\" table"):
                data_number = self.get_data_by_epa_region(table_name=table_name, epa_region=epa_region_id,
                                                          only_count=True, print_to_console=False)
                data_number_list.append(data_number)

        if print_to_console:
            header = ["EPA_REGION_ID", f"{table_name}_TOTAL_NUMBER"]
            tabulate_result = tabulate.tabulate(
                [[f"EPA_REGION_{i}", data_number_list[i - 1]] for i in EPA_REGION_ID],
                headers=header, numalign="right", stralign="right", tablefmt="simple_grid")
            print_tabulate_result_with_divider(tabulate_result)
        else:
            return data_number_list

    def get_data_by_epa_region(self, table_name="", epa_region=1, print_to_console=True, only_count=False,
                               multi_mode=False):
        """
        SAMPLE URL: https://data.epa.gov/efservice/LCR_SAMPLE/EPA_REGION/=/01/JSON
        :param multi_mode:
        :param table_name:
        :param only_count:
        :param epa_region:
        :param print_to_console:
        :param kwargs:
        :return:
        """
        _is_table_has_epa_region(table_name)
        _is_epa_region_param_valid(epa_region)
        column_name = "EPA_REGION"
        string_epa_region = f"0{epa_region}" if epa_region < 10 else epa_region
        query_url = f"{self.sdwis_api.base_url}/{table_name}/{column_name}/=/{string_epa_region}"
        if only_count:
            header = ["EPA_REGION_ID", f"{table_name}_TOTAL_NUMBER"]
            total_number = self.sdwis_api.get_request(query_url, only_count=only_count, multi_mode=multi_mode)
            if print_to_console:
                tabulate_result = tabulate.tabulate([[f"EPA_REGION_{string_epa_region}", total_number]], headers=header,
                                                    tablefmt="simple_grid")
                print_tabulate_result_with_divider(tabulate_result)
            return total_number
        else:
            return self._get_result_data_by_request(query_url, print_to_console=print_to_console)
