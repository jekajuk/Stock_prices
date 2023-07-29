import time
from threading import Thread, Lock
from Tools import *
from InputDataPreparation import *
from InputDataReader import *

"""     
        !!!! Input args --stat_sign and --size_step are decimal fraction, not percent !!!    
"""

# input_args_file_path = [{'-f': 'input_args.txt'}]

start_time = time.time()
process_start_time = time.process_time()

lock = Lock()
thread_pool = []
data = Data()

# -----------   Reading and converting input args     ---------------
work_args = reading_and_preparing_input_parameters()
# -----------   Reading input data from CSV file    ---------------
read_input_data_from_file(work_args, data)
# -----------   Reading input data from API     ---------------
# read_input_data_from_api(work_args, data)
# -----------   Input data preparation      ---------------
new_work_args = prepare_data_and_correct_input_args(data, work_args)
# -----------   Calculation dynamic of stock prices by threads
for thread_num, args in enumerate(new_work_args):
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
