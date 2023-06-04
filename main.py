import Tools
from Data import Data

data = Data()
file_path = 'input_args.txt'

# -----------------------Version 3 - read args from TXT file ------------------------------
arguments_dictionary = Tools.glob_arguments_reader_to_dictionary(file_path)
args = arguments_dictionary
print(arguments_dictionary)
Tools.read_csv_to_list(args['-f'], data)
Tools.adding_missing_information(data)
Tools.clean_unnecessary_data(data)
Tools.sort_by_year_to_dictionary(int(args['--y_min']), int(args['--y_max']), data)
Tools.prices_comparison_average_ss_calculation(int(args['--n_min']), int(args['--n_max']), int(args['--y_min']),
                                               int(args['--y_max']), data, float(args['--stat_sign']),
                                               float(args['--size_step']))
print(*data.result_data, sep="\n")


# -----------------------Version 2 - added reader args from cmd line ------------------------------
#
# args_list = Tools.cmd_args_reader()
# Tools.read_csv_to_list(args_list[0], data)
# Tools.adding_missing_information(data)
# Tools.clean_unnecessary_data(data)
# Tools.sort_by_year_to_dictionary(args_list[3], args_list[4], data)
# Tools.prices_comparison_average_ss_calculation(args_list[1], args_list[2], args_list[3], args_list[4],
#                                                data, args_list[5], args_list[6])
# print(*data.result_data, sep="\n")


# -----------------------Version 1  ------------------------------

# Tools.read_csv_to_list(file_path, data)
# Tools.adding_missing_information(data)
# Tools.clean_unnecessary_data(data)
# Tools.sort_by_year_to_dictionary(y_min, y_max, data)
# Tools.prices_comparison_average_ss_calculation(N_MIN, N_MAX, y_min, y_max,
#                                                data, stat_sign, step_of_size)
# print(*data.result_data, sep="\n")

# [file_path, N_MIN, N_MAX, y_min, y_max, stat_sign, step_of_size]