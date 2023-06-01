import Tools
from Data import Data

data = Data()

args_list = Tools.cmd_args_reader()
Tools.read_csv_to_list(args_list[0], data)
Tools.adding_missing_information(data)
Tools.clean_unnecessary_data(data)
Tools.sort_by_year_to_dictionary(args_list[3], args_list[4], data)
Tools.prices_comparison_average_ss_calculation(args_list[1], args_list[2], args_list[3], args_list[4],
                                               data, args_list[5], args_list[6])
print(*data.result_data, sep="\n")
