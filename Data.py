class Data:
    def __init__(self):  # add address csv
        self.first_date = 1
        self.last_date = 1
        self.input_data_list = {}
        self.sorted_data_list = {}
        self.result_data = []
        self.range_of_years = {}


# main.py  -f=TSLA    --n_min=15 --n_max=60
# --y_min=2011 --y_max=2020 --stat_sign=0.9 --size_step=0.04
#
# main.py  -f=TSLA    --n_min=15 --n_max=60 --y_min=2011 --y_max=2020 --stat_sign=0.9 --size_step=0.04
