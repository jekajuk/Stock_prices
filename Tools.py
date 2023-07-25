import argparse
from Data import Data

data = Data()


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


def positive_fraction_checker(a):
    num = float(a)
    if num < 0 or num > 1:
        raise argparse.ArgumentTypeError('Invalid Value, must be in range [0;1]')
    return num

# def cmd_args_reader():
#     parser = argparse.ArgumentParser(description='Reading input arguments')
#     parser.add_argument("-f", type=str, help='Input file path')
#     parser.add_argument('--n_min', type=int, help='min date difference')
#     parser.add_argument('--n_max', type=int, help='max date difference')
#     parser.add_argument('--y_min', type=int, help='starting year')
#     parser.add_argument('--y_max', type=int, help='finish year')
#     parser.add_argument('--stat_sign', type=positive_fraction_checker, help='Fraction statistical significance')
#     parser.add_argument('--size_step', type=positive_fraction_checker, help='Fraction of size of step')
#     args = parser.parse_args()
#
#     file_path = args.f
#     N_MIN = args.n_min
#     N_MAX = args.n_max
#     y_min = args.y_min
#     y_max = args.y_max
#     stat_sign = args.stat_sign     # Statistical_significance
#     step_of_size = args.size_step    # step_of_size
#
#     args_list = [file_path, N_MIN, N_MAX, y_min, y_max, stat_sign, step_of_size]
#     # args_list.append(file_path)
#     # args_list.append(N_MIN)
#     # args_list.append(N_MAX)
#     # args_list.append(y_min)
#     # args_list.append(y_max)
#     # args_list.append(stat_sign)
#     # args_list.append(step_of_size)
#     return args_list


# 1 ----- Methods for reading args from file.txt, conversion to input dictionary
#         checking args if in right range, checking if input data file exist


# 3 ------------ Reading and preparation input data for analysis
