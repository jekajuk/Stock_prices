import os
import csv
from datetime import timedelta, datetime
from Data import Data
import requests
data = Data()


# 1 ----- Methods for reading args from file.txt, conversion to input dictionary
#         checking args if in right range, checking if input data file exist
def read_input_args_from_file_to_dict(file_path):
    """Read input args from file.txt to dictionary"""
    temp_list = []
    input_args = []
    with open(file_path) as f:
        for line in f:
            if not line.isspace():
                temp_list.append(args_from_str_to_dict(line))
    for i in range(1, len(temp_list)):
        input_args.append(temp_list[0] | temp_list[i])          # merge two lines in list to get input args
    return input_args


def args_from_str_to_dict(input_string):
    """Convert string of input args  to dictionary"""
    res = []
    temp = input_string.replace("\n", "")                         # clean from '\n'
    temp_list = temp.split(sep="=")                        # split string to list by '='
    new_string = " ".join(temp_list)                      # Create new temp string
    args_list = new_string.split(sep=" ")                   # Split string to list by " " (whitespace)
    for item in args_list:                                  # Clean list from " " (whitespace)
        if item.strip():
            res.append(item)
    args_dict = {res[i]: res[i+1] for i in range(0, len(res), 2)}
    return args_dict


# 2 ----- Method for checkin args and conversion to int ant float
def convert_and_check_input_args(args_list):
    """Function checking if file with input args exist,
       convert from str to int and float,
       check if args in right range
       !!!! --stat_sign and --size_step are decimal fraction not percent !!!
    """
    work_args = []
    wrong_args = []
    for line in args_list:
        correct_values = True

        line['--n_min'] = abs(int(line['--n_min']))
        if line['--n_min'] < 1:
            print(f"--n_min must be > 1, your value is {float(line['--n_min'])}.")
            correct_values = False

        line['--n_max'] = abs(int(line['--n_max']))
        if line['--n_max'] < 1:
            print(f"--n_max must be > 1, your value is {float(line['--n_max'])}.")
            correct_values = False

        if line['--n_min'] > line['--n_max']:
            print(f"--n_max must be larger than --n_min, your values are --n_min = {line['--n_min']}, "
                  f"--n_max = {line['--n_max']}.")
            correct_values = False

        line['--y_min'] = abs(int(line['--y_min']))
        if line['--y_min'] < 1900:
            print(f"--y_min must be > 1900, your value is {float(line['--y_min'])}.")
            correct_values = False

        line['--y_max'] = abs(int(line['--y_max']))
        if line['--y_max'] < 1900:
            print(f"--y_max must be > 1900, your value is {float(line['--y_max'])}.")
            correct_values = False

        if line['--y_max'] < line['--y_min']:
            print("Argument '--y_max' can not less then '--y_min'.")
            correct_values = False

        line['--stat_sign'] = abs(float(line['--stat_sign']))
        if line['--stat_sign'] > 1:
            print(f"--stat_sign must be in range [0, 1], your value is {float(line['--stat_sign'])}.")
            correct_values = False

        line['--size_step'] = float(line['--size_step'])
        # TODO Is it have to be in this range?
        if line['--size_step'] < -1 or line['--size_step'] > 1:
            print(f"--stat_sign must be in range [-1, 1], your value is {float(line['--size_step'])}.")
            correct_values = False

        # TODO convert string to upper case
        # For version with API it doesn't work
        # if not os.path.exists(line['-f']):
        #     print(f"File {(line['-f'])} is not exist.")
        #     correct_values = False

        if correct_values:
            work_args.append(line)
        else:
            wrong_args.append(line)

    if len(wrong_args) != 0:
        print(f'\nSubsequent iterations will not be performed due to incorrect input arguments:')
        print(*wrong_args, sep='\n')

    return work_args


def prepare_reading_list(work_input_args):
    """For case  running analyses from csv files.
    Function collect names of files and range of years of data to be read from files"""
    reading_list = {}
    for line in work_input_args:
        if line['-f'] in reading_list:
            if line['--y_min'] < reading_list[line['-f']]['--y_min']:
                reading_list[line['-f']]['--y_min'] = line['--y_min']
            if line['--y_max'] > reading_list[line['-f']]['--y_max']:
                reading_list[line['-f']]['--y_max'] = line['--y_max']
        else:
            reading_list[line['-f']] = {'--y_min': line['--y_min'], '--y_max': line['--y_max']}
    return reading_list


def read_data_from_alphavantage(reading_list, data_obj):
    """Download stock data of companies from www.alphavantage.co"""
    date_format = '%Y-%m-%d'
    base_url = 'https://www.alphavantage.co/query?'
    for item in reading_list:
        temp_list = []
        params = {'function': 'TIME_SERIES_DAILY_ADJUSTED',
                  'outputsize': 'full',                  # compact = 100, full - all history
                  'symbol': item,
                  'apikey': 'NKXVSX4WW8L3XNXY'}              # Need to get your key

        response = requests.get(base_url, params=params)
        for date in response.json()['Time Series (Daily)']:
            temp_row = [datetime.strptime(date, date_format).date(),
                        float(response.json()['Time Series (Daily)'][date]['4. close'])]
            temp_list.append(temp_row)
        data_obj.input_data_list[item] = temp_list


# 3 ------------ Reading and preparation input data for analysis
def read_csv_to_list(work_args, data_obj):  # read csv to data object list
    """Function reading input data from csv file and saving to data_obj.input_data_list"""
    date_format = '%d/%m/%Y'
    for line in work_args:
        # print(work_args[line])
        temp_list = []
        with open(line) as data_file:
            data_list = csv.reader(data_file)

            for row in data_list:
                row[0] = datetime.strptime(row[0], date_format).date()
                if row[0].year > work_args[line]['--y_max']:
                    break
                elif row[0].year < work_args[line]['--y_min']:
                    continue
                else:
                    row[1] = float(row[1])
                    temp_list.append(row)
        data_obj.input_data_list[line] = temp_list


def adding_missing_information(data_obj):
    """ Function checking difference between dates and adding
    missing information (Dates and Prices). Missing price is price one day before"""
    for company in data_obj.input_data_list:
        if data_obj.input_data_list[company][0][0] > data_obj.input_data_list[company][-1][0]:
            data_obj.input_data_list[company].reverse()
        for index, value in enumerate(data_obj.input_data_list[company]):
            if index + 1 < len(data_obj.input_data_list[company]):
                delta = data_obj.input_data_list[company][index + 1][0] - data_obj.input_data_list[company][index][0]
                if delta.days > 1:
                    new_date = data_obj.input_data_list[company][index][0] + timedelta(days=1)
                    new_price = data_obj.input_data_list[company][index][1]
                    new_list = [new_date, new_price]
                    data_obj.input_data_list[company].insert(index + 1, new_list)


def sort_to_dict(data_obj):
    """ Functon sort input data by years and save to
    dictionary {company_1: {year_1: [stock prices,..], year_2: [stock prices,..]},
    company_2: {year_1: [stock prices,..], year_2: [stock prices,..]} }"""
    for company in data_obj.input_data_list:
        if company not in data_obj.sorted_data_list:
            data_obj.sorted_data_list[company] = {}
        for row in data_obj.input_data_list[company]:
            if row[0].year not in data_obj.sorted_data_list[company]:
                data_obj.sorted_data_list[company][row[0].year] = {}
                data_obj.sorted_data_list[company][row[0].year] = [row]
            else:
                data_obj.sorted_data_list[company][row[0].year].append(row)


def check_leap_year(year):
    """Boolean function check if year is leap """
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def clean_unnecessary_data(data_obj):
    """Clean from date sorted list of data dates:
     01/01, 29/02, 04/07, 25/12, Summary file cleaning"""

    if os.path.exists('Summary'):
        with open('Summary', 'w'):
            pass
    for company in data_obj.sorted_data_list:
        # print(company)
        for year in data_obj.sorted_data_list[company]:
            n = data_obj.sorted_data_list[company][year][0][0].timetuple().tm_yday
            first_jan_index = 1 - n
            len_of_data_list = len(data_obj.sorted_data_list[company][year])
            # print(f'{year}: length {len_of_data_list}')
            if check_leap_year(year):
                if first_jan_index == 0 and first_jan_index <= len_of_data_list:
                    # print(data_obj.sorted_data_list[company][year][first_jan_index])
                    del data_obj.sorted_data_list[company][year][first_jan_index]
                    n += 1
                    len_of_data_list -= 1
                twenty_nine_feb_index = 60 - n
                if 0 <= twenty_nine_feb_index <= len_of_data_list:
                    # print(data_obj.sorted_data_list[company][year][twenty_nine_feb_index])
                    del data_obj.sorted_data_list[company][year][twenty_nine_feb_index]
                    n += 1
                    len_of_data_list -= 1
                fourth_jul_index = 186 - n
                if 0 <= fourth_jul_index <= len_of_data_list:
                    # print(data_obj.sorted_data_list[company][year][fourth_jul_index])
                    del data_obj.sorted_data_list[company][year][fourth_jul_index]
                    n += 1
                    len_of_data_list -= 1
                twenty_five_dec_index = 360 - n
                if 0 <= twenty_five_dec_index <= len_of_data_list:
                    # print(data_obj.sorted_data_list[company][year][twenty_five_dec_index])
                    del data_obj.sorted_data_list[company][year][twenty_five_dec_index]
            else:
                if first_jan_index == 0 and first_jan_index <= len_of_data_list:
                    # print(data_obj.sorted_data_list[company][year][first_jan_index])
                    del data_obj.sorted_data_list[company][year][first_jan_index]
                    n += 1
                    len_of_data_list -= 1
                fourth_jul_index = 185 - n
                if 0 <= fourth_jul_index <= len_of_data_list:
                    # print(data_obj.sorted_data_list[company][year][fourth_jul_index])
                    del data_obj.sorted_data_list[company][year][fourth_jul_index]
                    n += 1
                    len_of_data_list -= 1
                twenty_five_dec_index = 359 - n
                if 0 <= twenty_five_dec_index <= len_of_data_list:
                    # print(data_obj.sorted_data_list[company][year][twenty_five_dec_index])
                    del data_obj.sorted_data_list[company][year][twenty_five_dec_index]


def clean_partial_year_data(data_obj):
    """Delete from dictionary partial annual data"""
    years_to_be_removed = {}
    for company in data_obj.sorted_data_list:
        for year in data_obj.sorted_data_list[company]:
            if len(data_obj.sorted_data_list[company][year]) < 362:
                if company not in years_to_be_removed:
                    years_to_be_removed[company] = {}
                    years_to_be_removed[company] = [year]
                else:
                    years_to_be_removed[company].append(year)
    for company in years_to_be_removed:
        for year in years_to_be_removed[company]:
            del data_obj.sorted_data_list[company][year]


def correct_work_args(data_obj, work_args):
    """Correct input args y_min and y_max after preparing input data for analyses,
     delete input args if y_max <= y_min"""
    correction_list = {}
    wrong_args = []
    for company in data_obj.sorted_data_list:
        # y_min = min(data_obj.sorted_data_list[company])
        # y_max = max(data_obj.sorted_data_list[company])
        correction_list[company] = {'y_min': min(data_obj.sorted_data_list[company]),
                                    'y_max': max(data_obj.sorted_data_list[company])}

    for company in correction_list:
        for row in work_args:
            if company == row['-f']:
                if row['--y_min'] < correction_list[company]['y_min']:
                    row['--y_min'] = correction_list[company]['y_min']
                if row['--y_max'] > correction_list[company]['y_max']:
                    row['--y_max'] = correction_list[company]['y_max']
                if row['--y_max'] - row['--y_min'] < 1:
                    wrong_args.append(row)
                    work_args.remove(row)

    if len(wrong_args) != 0:
        print(f'\nSubsequent iterations will not be performed due to incorrect input arguments:')
        print(*wrong_args, sep='\n')


def prices_comparison_average_ss_calculation(input_args, data_obj, lock, thr_num):
    """ Function checking dynamic of stock prices """
    print(f'Thread {thr_num} started')
    result_data = []
    company = input_args['-f']
    n_min = input_args['--n_min']
    n_max = input_args['--n_max']
    y_min = input_args['--y_min']
    y_max = input_args['--y_max']
    stat_sign = input_args['--stat_sign']
    step_of_size = input_args['--size_step']
    for i in range(0, 362):
        for n in range(n_min, n_max + 1):
            positive_delta = []
            negative_delta = []
            if i + n < 362:
                for year in range(y_min, y_max):
                    n1 = data_obj.sorted_data_list[company][year][i][1]
                    n2 = data_obj.sorted_data_list[company][year][i + n][1]
                    delta = ((n2 - n1) / n1)
                    # print(f'{delta} + {year} + {n}')
                    if delta > 0:
                        positive_delta.append(delta)
                    if delta < 0:
                        negative_delta.append(delta)
                if len(positive_delta) / (y_max - y_min + 1) >= stat_sign:
                    average = sum(positive_delta) / len(positive_delta)
                    if average > step_of_size:
                        result_data.append([average, i, n, data_obj.sorted_data_list[company][year][i][0],
                                            f'Thread: {thr_num}'])
                if len(negative_delta) / (y_max - y_min + 1) >= stat_sign:
                    average = sum(negative_delta) / len(negative_delta)
                    if average < -step_of_size:
                        result_data.append([average, i, n, data_obj.sorted_data_list[company][year][i][0],
                                            f'Thread: {thr_num}'])
    lock.acquire()
    with open('Summary', 'a') as f:
        # f.write(f'Thread {thr_num} \n')
        for key, value in input_args.items():
            f.write('%s:%s, ' % (key, value))
        f.write('\n')
        for line in result_data:
            f.writelines(f'{line}\n')
        f.writelines(f'\n\n\n\n\n')
    lock.release()
    data.result_data.append(result_data)
    print(f'Thread {thr_num} finished')
    return result_data
