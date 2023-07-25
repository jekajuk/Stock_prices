from Data import Data
import os.path
import sys

data = Data()


def reading_and_preparing_input_parameters(input_string=None):
    """Function read input args from cmd or file path with input args,
     convert args values to int, float, check if file exist and checkin
      args values range
      \nInput: args from cmd.
      Output: <dict><list><dict>:
       {
       'file_run':[{'-f': str, '--n_min': int, ...,'--stat_sign': float },.., {}],
       'api_run':[{'-f': str, '--n_min': int, ...,'--stat_sign': float },.., {}]
       }
       or stop program if not enough input params."""
    if input_string is None:
        # -----------   Reading and converting input args  ---------------
        # Convert input args in cmd to <list><dict> [{'-f':str, '--n_min': str, ...etc. }]
        input_args = [read_input_args_from_cmd()]
    else:
        input_args = input_string
    # Convert input args from str to int, float, checking range, if file exist and
    # sort for file run data  and api run data.
    work_args = prepare_work_args_list(input_args)
    if not len(work_args['file_run']) and not len(work_args['api_run']):
        print('\nAfter checking input args there are no arguments to run program.')
        exit()
    return work_args


# ----------------------------------------------------------
def read_input_args_from_cmd():
    """Function read input args from cmd.
    \nInput: args entered in cmd.
    \nOutput: <dict> of input args.
             {'-f':str, '--n_min': str, ...etc. }"""
    cmd_args_input = sys.argv
    del cmd_args_input[0]
    input_string = " ".join(cmd_args_input)
    input_args = args_from_str_to_dict(input_string)
    print(input_args)
    print(len(input_args))
    return input_args


def args_from_str_to_dict(input_string):
    """Convert string of input args  to dictionary
    \nInput: <string> of args
    Output: <dict> {'-f':str, '--n_min': str, ...etc. }"""
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


# ----------------------------------------------------------
def prepare_work_args_list(input_list):
    """Function converting and checking input args from list.
    \n If len(input_list) == 7 function converting and checking input args from list
    Input: <list><dict> [{'-f':str, '--n_min': str, ...,'--stat_sign': str }]
    Output: <dict><list><dict> {'file_run':[{'-f':str, '--n_min': int, ...,'--stat_sign': float }]}
    \n If len(input_list) == 1 function read input args from file in path ('-f'), converting and checking
     input args from list.
     Input: <list><dict> [{'-f': str}]
     Output: <dict><list><dict>:
       {
       'file_run':[{'-f': str, '--n_min': int, ...,'--stat_sign': float },.., {}],
       'api+run':[{'-f': str, '--n_min': int, ...,'--stat_sign': float },.., {}]
       }
    \nIn other cases function stop program.
     """
    if len(input_list[0]) == 7:
        return convert_and_check_input_args(input_list)
    elif len(input_list[0]) == 1:
        if '-f' in input_list[0]:
            if os.path.exists(input_list[0]['-f']):
                input_args_from_file = read_input_args_from_file_to_dict(input_list[0]['-f'])
                return convert_and_check_input_args(input_args_from_file)
            else:
                print(f"File '-f' {input_list[0]['-f']} doesn't exist. Program stop to run.")
                exit()
        else:
            print(f"Need input argument '-f'")
            exit()
    else:
        print("Not enough arguments.\nProgram stop to run.\nNumber of arguments must be 1 ('-f') or 7.")
        exit()


# 2 ----- Method for checkin args and conversion to int ant float
def convert_and_check_input_args(args_list):
    """Function checking if file with input args exist,
       convert from str to int and float,
       check if args in right range and sort for file run data  and api run data.
       !!!! --stat_sign and --size_step are decimal fraction not percent !!!
       \nInput:<list> of <dict> of input args:
       [{'-f':str, '--n_min': str, ...,'--stat_sign': str },.., {}]
       \nOutput: <dict> of <list> of <dict>:
       {
       'file_run':[{'-f':str, '--n_min': int, ...,'--stat_sign': float },.., {}],
       'api+run':[{'-f':str, '--n_min': int, ...,'--stat_sign': float },.., {}]
       }

    """
    work_args = {'file_run': [], 'api_run': []}
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
        # # TODO Does it have to be in this range?
        # if line['--size_step'] < -1 or line['--size_step'] > 1:
        #     print(f"--stat_sign must be in range [-1, 1], your value is {float(line['--size_step'])}.")
        #     correct_values = False

        # TODO convert string to upper case
        # # For version with API it doesn't work
        # if not os.path.exists(line['-f']):
        #     print(f"File {(line['-f'])} does not exist.")
        #     correct_values = False

        if correct_values and os.path.exists(line['-f']):
            work_args['file_run'].append(line)
        elif correct_values and not os.path.exists(line['-f']):
            work_args['api_run'].append(line)
        else:
            wrong_args.append(line)

    if len(wrong_args) != 0:
        print(f'\nSubsequent iterations will not be performed due to incorrect input arguments:')
        print(*wrong_args, sep='\n')

    return work_args


def read_input_args_from_file_to_dict(file_path):
    """Read input args from file.txt to dictionary
    Input: <str> file path
    Output: <list> of <dict> [{'-f':str, '--n_min': str, ...etc. }, {}, ...etc.]"""
    temp_list = []
    input_args = []
    with open(file_path) as f:
        for line in f:
            if not line.isspace():
                temp_list.append(args_from_str_to_dict(line))
    for i in range(1, len(temp_list)):
        input_args.append(temp_list[0] | temp_list[i])          # merge two lines in list to get input args
    return input_args


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
        print(f"\nSubsequent iterations after correction will "
              f"not be performed due to incorrect values '--y_min' and '--y_max':")
        print(*wrong_args, sep='\n')
    return work_args
