import time
from threading import Thread, Lock

from Data import Data
from Tools import *

"""     
        !!!! Input args --stat_sign and --size_step are decimal fraction, not percent !!!    
"""

start_time = time.time()
process_start_time = time.process_time()

data = Data()
input_args_file_path = 'input_args.txt'

lock = Lock()
thread_pool = []

input_args_from_file = read_input_args_from_file_to_dict(input_args_file_path)
work_args = convert_and_check_input_args(input_args_from_file)
reading_list = {line['-f'] for line in work_args}
read_data_from_alphavantage(reading_list, data)
adding_missing_information(data)
sort_to_dict(data)
clean_unnecessary_data(data)
clean_partial_year_data(data)
correct_work_args(data, work_args)

for thread_num, args in enumerate(work_args):
    thread = Thread(target=prices_comparison_average_ss_calculation, args=(args, data, lock, thread_num))
    thread_pool.append(thread)

# Start the threads
for thread in thread_pool:
    thread.start()

# Wait for all threads to finish
for thread in thread_pool:
    thread.join()

end_time = time.time()
process_end_time = time.process_time()

elapsed_time = end_time - start_time
cpu_time = process_end_time - process_start_time
print('Execution time:', elapsed_time, 'seconds')
print('CPU execution time:', cpu_time, 'seconds')
