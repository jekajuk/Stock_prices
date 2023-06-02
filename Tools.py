import csv
from datetime import timedelta, datetime
from Data import Data
import argparse

data = Data()


def positive_fraction_checker(a):
    num = float(a)
    if num < 0 or num > 1:
        raise argparse.ArgumentTypeError('Invalid Value, must be in range [0;1]')
    return num


def cmd_args_reader():
    parser = argparse.ArgumentParser(description='Reading input arguments')
    parser.add_argument("-f", type=str, help='Input file path')
    parser.add_argument('--n_min', type=int, help='min date difference')
    parser.add_argument('--n_max', type=int, help='max date difference')
    parser.add_argument('--y_min', type=int, help='starting year')
    parser.add_argument('--y_max', type=int, help='finish year')
    parser.add_argument('--stat_sign', type=positive_fraction_checker, help='Fraction statistical significance')
    parser.add_argument('--size_step', type=positive_fraction_checker, help='Fraction of size of step')
    args = parser.parse_args()

    file_path = args.f
    N_MIN = args.n_min
    N_MAX = args.n_max
    y_min = args.y_min
    y_max = args.y_max
    stat_sign = args.stat_sign     # Statistical_significance
    step_of_size = args.size_step    # step_of_size

    args_list = [file_path, N_MIN, N_MAX, y_min, y_max, stat_sign, step_of_size]
    # args_list.append(file_path)
    # args_list.append(N_MIN)
    # args_list.append(N_MAX)
    # args_list.append(y_min)
    # args_list.append(y_max)
    # args_list.append(stat_sign)
    # args_list.append(step_of_size)
    return args_list


def read_csv_to_list(file_name, data):  # read csv to data object list
    date_format = '%d/%m/%Y'
    with open(file_name) as data_file:
        data_list = csv.reader(data_file)
        for row in data_list:
            row[0] = datetime.strptime(row[0], date_format).date()
            row[1] = float(row[1])
            data.input_data_list.append(row)


def adding_missing_information(data):  # ADDING  MISSING INFORMATION TO LIST (Dates and Prices)
    for index, value in enumerate(data.input_data_list):
        if index + 1 < len(data.input_data_list):
            delta = data.input_data_list[index + 1][0] - data.input_data_list[index][0]
            if delta.days > 1:
                new_date = data.input_data_list[index][0] + timedelta(days=1)
                new_price = data.input_data_list[index][1]
                new_list = [new_date, new_price]
                data.input_data_list.insert(index + 1, new_list)


def clean_unnecessary_data(data):  # Clean 01.01 / 29.02 / 04.07 / 25.12      ##########################
    for row in data.input_data_list:
        if row[0].month == 1 and row[0].day == 1:
            data.input_data_list.remove(row)
        if row[0].month == 2 and row[0].day == 29:
            data.input_data_list.remove(row)
        if row[0].month == 7 and row[0].day == 4:
            data.input_data_list.remove(row)
        if row[0].month == 12 and row[0].day == 25:
            data.input_data_list.remove(row)


def sort_by_year_to_dictionary(y_min, y_max, data):  # Sort data by year and adding to dictionary
    for year in range(y_min, y_max + 1):
        temp_list = []
        for row in data.input_data_list:
            if row[0].year == year:
                temp_list.append(row)
        data.sorted_data_list[year] = temp_list


def prices_comparison_average_ss_calculation(n_min, n_max, y_min, y_max, data, stat_sign, step_of_size):
    for i in range(0, 362):
        for n in range(n_min, n_max + 1):
            positive_delta = []
            negative_delta = []
            if i + n < 362:
                for year in range(y_min, y_max + 1):
                    n1 = data.sorted_data_list[year][i][1]
                    n2 = data.sorted_data_list[year][i + n][1]
                    delta = ((n2 - n1) / n1)
                    # print(f'{delta} + {year} + {n}')
                    if delta > 0:
                        positive_delta.append(delta)
                    if delta < 0:
                        negative_delta.append(delta)
                if len(positive_delta) / (y_max - y_min + 1) >= stat_sign:
                    average = sum(positive_delta) / len(positive_delta)
                    if average > step_of_size:
                        data.result_data.append([average, i, n, data.sorted_data_list[year][i][0]])
                if len(negative_delta) / (y_max - y_min + 1) >= stat_sign:
                    average = sum(negative_delta) / len(negative_delta)
                    if average < -step_of_size:
                        data.result_data.append([average, i, n, data.sorted_data_list[year][i][0]])


class Tools:
    pass
