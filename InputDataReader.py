import csv
from datetime import datetime
import requests


def read_input_data_from_file(work_args, data_obj):
    if len(work_args['file_run']):
        reading_list_from_csv = prepare_reading_list(work_args['file_run'])
        print(type(reading_list_from_csv))
        read_csv_to_list(reading_list_from_csv, data_obj)
    else:
        print("No files in reading list.")


def read_input_data_from_api(work_args, data_obj):
    if len(work_args['api_run']):
        reading_list_from_api = prepare_reading_list(work_args['api_run'])
        # reading_list_from_api = {line['-f'] for line in work_args['api+run']}
        read_data_from_api_alphavantage(reading_list_from_api, data_obj)
    else:
        print("No data to read from api.")


def prepare_reading_list(work_input_args):
    """For case  running analyses from csv files.
    Function collect names of files and range of years of data to be read from files
    \nInput: <list> of <dict> [{'-f':str, '--n_min': int, ...,'--stat_sign': float },.., {}]
    Output: <dict> of <dict>:
            {
            file_name_1: {'y_min': int, 'y_max': int},
            file_name_2: {'y_min': int, 'y_max': int}, ..etc
            }"""
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


def read_csv_to_list(work_args, data_obj):  # read csv to data object list
    """Function reading input data from csv file and saving to data_obj.input_data_list
    \ninput: <dict> of <dict>:
            {
            file_name_1: {'y_min': int, 'y_max': int},
            file_name_2: {'y_min': int, 'y_max': int}, ..etc
            }
    \nOutput: <dict> of <list> saved in data_obj.input_data_list.
            {
            'INTC': [stock prices data],
            'TSLA': [stock prices data]
            }
    """
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


def read_data_from_api_alphavantage(reading_list, data_obj):
    """Download stock data of companies from www.alphavantage.co
    input: <tuple> of company indexes, for example {INTC, TSLA}
    Output: <dict> of <list> saved in data_obj.input_data_list.
            {
            'INTC': [stock prices data],
            'TSLA': [stock prices data]
            }"""
    date_format = '%Y-%m-%d'
    base_url = 'https://www.alphavantage.co/query?'
    for item in reading_list:
        temp_list = []
        params = {'function': 'TIME_SERIES_DAILY_ADJUSTED',
                  'outputsize': 'full',  # compact = 100, full - all history
                  'symbol': item,
                  'apikey': 'NKXVSX4WW8L3XNXY'}  # Need to get your key

        response = requests.get(base_url, params=params)
        for date in response.json()['Time Series (Daily)']:
            temp_row = [datetime.strptime(date, date_format).date(),
                        float(response.json()['Time Series (Daily)'][date]['4. close'])]
            temp_list.append(temp_row)
        data_obj.input_data_list[item] = temp_list
