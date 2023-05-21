import Tools
from Data import Data

data = Data()
file_name_1 = 'AA raw data 11.csv'
file_name_2 = 'sample raw data.csv'

N_MIN = 15
N_MAX = 60

y_min = 2000
y_max = 2020

Tools.read_csv_to_list(file_name_1, data)
Tools.adding_missing_information(data)
Tools.clean_unnecessary_data(data)
Tools.sort_by_year_to_dictionary(y_min, y_max, data)
Tools.prices_comparison_average_ss_calculation(N_MIN, N_MAX, y_min, y_max, data)
print(*data.result_data, sep="\n")
