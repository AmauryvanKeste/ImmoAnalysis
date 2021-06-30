import pandas as pd
import numpy as np
# conda install multipledispatch
# from multipledispatch import dispatch


class DfOps:

    def __init__(self, dataframe, max_cols, cons_width=640):
        self.df = dataframe
        self.df.sort_index()
        self.initiate_pandas(max_cols, cons_width)
        self.initiate_numpy(cons_width)

    @staticmethod
    def initiate_pandas(max_cols, cons_width):
        pd.set_option('display.max_columns', max_cols)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', cons_width)  # make output in console wider

    @staticmethod
    def initiate_numpy(console_width=640):
        # https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html
        np.set_printoptions(linewidth=console_width)

    def rename_columns_dict(self, new_names: dict):
        self.df.rename(columns=new_names, inplace=True)

    def replace_value_in_column(self, column, old_value, new_value):
        self.df[column] = self.df[column].replace(to_replace=old_value, value=new_value)

    def change_zero_ones_to_true_false(self, columns_list: list):
        for column in columns_list:
            self.replace_value_in_column(column, 0, False)
            self.replace_value_in_column(column, 1, True)

    def change_no_yes_to_false_true(self, columns_list):
        for column in columns_list:
            self.replace_nan_in_column(column, "no")
            self.replace_value_in_column(column, "no", False)
            self.replace_value_in_column(column, "yes", True)

    def count_nans_in_column(self, column: str) -> int:
        return self.df[column].isna().sum()

    # convert to datatype only
    def convert_cols_to_datatype(self, columns, set_datatype_to):
        for col in columns:
            self.df[col] = self.df[col].astype(set_datatype_to)

    # fillna and convert to datatype
    def convert_cols_to_datatype_and_do_fillna(self, columns, fill_na_value, set_datatype_to=None):
        # do fillna AND convert to datatype
        if fill_na_value and set_datatype_to:
            for index, column in enumerate(columns):
                self.df[column] = self.df[column].fillna(fill_na_value).astype(set_datatype_to)

    # do fillna only
    def apply_fillna_to_column(self, column, replace_nan_value):
        self.df[column] = self.df[column].fillna(replace_nan_value)

    def replace_nan_in_column(self, columns, replace_nan_value):
        if not isinstance(columns, list):
            list(columns)
        self.apply_fillna_to_column(columns, replace_nan_value)

    # def convert_nan_to_datatype(self, columns, replace_nan_val, datatype):
    #     self.convert_cols_to_datatype_and_do_fillna(columns, replace_nan_val, datatype)

    # https://hashtaggeeks.com/posts/pandas-categorical-data.html
    @staticmethod
    def create_category(category_list):
        try:
            return pd.CategoricalDtype(categories=category_list)
        except Exception as err:
            print(f"something went wrong when creating categorical: {err}")

    def apply_mean_to_column(self, column):
        self.apply_fillna_to_column(column, self.df[column].mean())

    def write_to_csv(self, file_path):
        self.df.to_csv(file_path)

    def count_nans_in_df(self):
        return self.df.isna().sum()

    def print_datatypes(self):
        print("------------checking column datatypes------------>")
        print(self.df.dtypes)
        print("----------checking column datatypes END---------->")

    def print_columns_has_nan_check(self):
        print("----- columns with missing values = True -------->")
        print(self.df.isnull().any())
        print("----------- missing values check END ------------>")
