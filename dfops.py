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


import matplotlib.pyplot as plt
import seaborn as sns
import pathlib


class ChartMaker:
    default_path = pathlib.PurePath("files", "charts")

    def __init__(self, data, title, cm="Blues_d", palette="Blues_d", style="whitegrid"):
        self.data = data
        self.chart_style = style
        self.palette = palette
        self.cm = sns.color_palette(cm)
        self.title = title
        self.plot = plt
        self.figure = plt.figure()

    def get_correlation_matrix(self):
        if isinstance(self.data, pd.DataFrame):
            return self.data.corr().abs()

    def set_sns_theme_style(self):
        sns.set_theme(style=self.chart_style)

    # https://seaborn.pydata.org/generated/seaborn.heatmap.html?highlight=heatmap#seaborn.heatmap
    def create_sns_heatmap(self, matrix):
        sns.heatmap(matrix, cmap=self.cm)

    # https://seaborn.pydata.org/generated/seaborn.barplot.html?highlight=barplot#seaborn.barplot
    def create_sns_barplot(self, y_title: str):
        sns.barplot(x=self.data.index, y=y_title, data=self.data, palette=self.palette)

    def set_figure_title(self, title: str, fontsize=9):
        self.figure.suptitle(title)

    def set_plot_title(self, title: str):
        self.plot.title(title)

    def save_plot_figure(self, filename: str):
        save_final = pathlib.PurePath(self.default_path, filename)
        self.plot.savefig(save_final)

    def set_plot_figure_fize(self, x: int, y: int):
        self.figure.figsize(x, y)

    def plot_show_figures(self):
        self.plot.show()

    def set_plot_ylim(self, y_range_start: int, y_range_stop: int):
        # range allowed on y-axis
        self.plot.ylim(y_range_start, y_range_stop)

    def set_plot_ylabel(self, y_label: str):
        self.plot.ylabel(y_label)

    def set_yticks(self, start: int, stop: int, step: float):
        self.plot.yticks(np.arange(start, stop, step=step))