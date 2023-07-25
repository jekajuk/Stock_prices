from datetime import timedelta
from InputArgsReader import *
import os


def prepare_data_and_correct_input_args(data_obj, work_args):
    adding_missing_information(data_obj)
    sort_to_dict(data_obj)
    clean_unnecessary_data(data_obj)
    clean_partial_year_data(data_obj)
    temp_work_args = work_args['file_run'] + work_args['api_run']
    new_work_args = correct_work_args(data_obj, temp_work_args)
    # new_work_args = work_args['file_run'] + work_args['api_run']
    print('\nnew_work_args:')
    print(*new_work_args, sep='\n')
    correct_work_args(data, new_work_args)
    print('\nAfterCorrection:')
    print(*new_work_args, sep='\n')
    return new_work_args


def adding_missing_information(data_obj):
    """ Function checking difference between dates and adding
    missing information (Dates and Prices). Missing price is price one day before
    \nInput: data_obj.input_data_list
    Output: corrected data in data_obj.input_data_list"""
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
    company_2: {year_1: [stock prices,..], year_2: [stock prices,..]} }
    \n Input: data_obj.input_data_list
    Output: sorted data saved in data_obj.sorted_data_list"""
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
    """Boolean function check if year is leap
    \nInput: <int> year to check
    Output: <bool>: 'True' if year is leap, 'False' if year is not leap  """
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
     01/01, 29/02, 04/07, 25/12, Summary file cleaning
     \nInput: data_obj.sorted_data_list
     Output: corrected data in data_obj.sorted_data_list"""

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
