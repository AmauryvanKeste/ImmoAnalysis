def initiate_pandas(max_cols=20, console_width=640):
    try:
        import pandas as pd_custom
        pd_custom.set_option('display.max_columns', max_cols)
        pd_custom.set_option('display.max_rows', None)
        pd_custom.set_option('display.width', console_width)  # make output in console wider
        return pd_custom
    except ImportError:
        print("pandas not installed")


def initiate_numpy(console_width=640):
    # https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html
    try:
        import numpy as np_custom
        np_custom.set_printoptions(linewidth=console_width)
        return np_custom
    except ImportError:
        print("numpy not installed")


pd = initiate_pandas()
np = initiate_numpy()


def rename_columns_dict(dframe, d_newnames):
    dframe.rename(columns=d_newnames, inplace=True)


def replace_value_in_column(dframe, column, old_value, new_value):
    dframe[column] = dframe[column].replace(to_replace=old_value, value=new_value)


def change_zero_ones_to_true_false(dframe, columns_list):
    for column in columns_list:
        replace_value_in_column(dframe, column, 0, False)
        replace_value_in_column(dframe, column, 1, True)


def change_no_yes_to_false_true(dframe, columns_list):
    for column in columns_list:
        replace_nan_in_column(dframe,[column], "no")
        replace_value_in_column(dframe, column, "no", False)
        replace_value_in_column(dframe, column, "yes", True)


def count_nans_in_column(dframe, column):
    return dframe[column].isna().sum()


def replace_nan_in_column(dframe, columns_list, new_val):
    for column in columns_list:
        dframe[column] = dframe[column].fillna(new_val)


def convert_nan_to_datatype(dframe, columns_list, replace_nan_val, datatype):
    for column in columns_list:
        dframe[column] = dframe[column].fillna(replace_nan_val).astype(datatype)


# def change_nan_value_to_mean(dframe, columns_list):
#     for column in columns_list:
#         mean = dframe[column].mean()
#         print(mean)
#         print("==========")


def cast_to_datatype(dframe, column_list, datatype):
    for column in column_list:
        dframe[column] = dframe[column].astype(datatype)


# https://hashtaggeeks.com/posts/pandas-categorical-data.html
def create_category(category_list):
    try:
        return pd.CategoricalDtype(categories=category_list)
    except ValueError:
        print(f"something went wrong: {ValueError}")


def get_mean_for_column(dframe, column):
    print(f"mean for {column}: {dframe[column].mean()}")
    return dframe[column].mean()


def write_to_csv(dframe, file_path):
    dframe.to_csv(file_path)


def main():
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
    # read in all rows and from col1 till last column
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',').iloc[:, 1:]

    # sorting out of habit for performance
    df_houses.sort_index()

    # renaming columns for easy of use
    d_rename_cols_old_new = {
        "Area [m²]": "area",
        "Price [€]": "price",
        "state of the building": "building_state",
        "number of facades": "facades",
        "number of bedrooms": "bedrooms",
        "fully equipped kitchen": "kitchen_equipped",
        "open fire": "open_fire",
        "locality [zip code]": "locality",
        "surface of the land [m²]": "land_surface",
        "terrace surface [m²]": "terrace_surface",
        "swimming pool": "swimming_pool",
        "type of property": "property_type",
        "subtype of property": "property_subtype",
        "garden surface [m²]": "garden_surface"
    }
    rename_columns_dict(df_houses, d_rename_cols_old_new)

    # converting columns to dtype bool
    # todo: change yes no to true false before converting to bool
    # set 1"s to True and 0's to False for following columns
    booleanize_these_columns = ["garden", "terrace"]
    change_zero_ones_to_true_false(df_houses, booleanize_these_columns)
    yes_no_to_true_false = ["furnished", "swimming_pool"]
    change_no_yes_to_false_true(df_houses, yes_no_to_true_false)

    cols_that_change_to_bool_dtype = ["swimming_pool", "garden", "terrace", "furnished"]
    cast_to_datatype(df_houses, cols_that_change_to_bool_dtype, "bool")

    # change NaN to False for "swimming_pool" column
    replace_nan_in_column(df_houses, ["swimming_pool"], False)

    # replace "no" to "NaN" for price column
    replace_value_in_column(df_houses, "price", "no", np.NaN)
    cast_to_datatype(df_houses, ["facades", "bedrooms", "open_fire", "price"], "float64")
    # https://datatofish.com/rows-with-nan-pandas-dataframe/
    indexes_price_is_no = df_houses[df_houses["price"].isna()].index
    df_houses.drop(indexes_price_is_no, inplace=True)


    # replace exception to exceptional
    replace_value_in_column(df_houses, "property_subtype", "exceptiona", "exceptional")

    # change NaN to "undefined" for following columns
    change_nan_to_undefined = ["kitchen_equipped", "building_state", "property_subtype"]
    replace_nan_in_column(df_houses, change_nan_to_undefined, "undefined")



    # mixed dtypes conversion:
    #   df['col'] = pd.to_numeric(df['col'], errors='coerce')

    # create categoricals -> https://pandas.pydata.org/pandas-docs/stable/user_guide/categorical.html
    kitchen_equipped_cat = ['installed', 'undefined', 'hyper equipped', 'semi equipped', 'usa semi equipped',
                            'usa installed', 'usa hyper equipped', 'not installed', 'usa uninstalled']
    building_state_cat = ['good', 'just renovated', 'as new', 'to renovate', 'to be done up', 'to restore',
                          'undefined']
    property_type_cat = ['house', 'land', 'other']
    # apply undefined
    property_subtype_cat = ['house', 'villa', 'mixed', 'town', 'farmhouse', 'chalet',
                            'country', 'exceptional', 'building', 'apartment', 'mansion',
                            'bungalow', 'other', 'manor', 'castle', 'land', 'undefined']

    categories_column_d = {"kitchen_equipped": kitchen_equipped_cat,
                           "building_state": building_state_cat,
                           "property_type": property_type_cat,
                           "property_subtype": property_subtype_cat}

    # turn keys (columns) in categories_column_d dictionary into a Category
    for column, cat_list in categories_column_d.items():
        cat_type = create_category(cat_list)
        df_houses[column] = df_houses[column].astype(cat_type)

    # replace NaN's for every column in list with value returned by get_mean_for_column()
    columns_to_mean = ["area", "facades", "bedrooms", "price", "open_fire"]
    for column in columns_to_mean:
        mean = get_mean_for_column(df_houses, column)
        replace_nan_in_column(df_houses, [column], mean)

    # print data types to check successful conversion
    print("------------checking datatypes------------>")
    print(df_houses.dtypes)
    print("----------checking datatypes END---------->")

    print("----- confirm there are no missing values ------->")
    print(df_houses.isnull().any())  # True = missing values
    print("----------- missing values check END ------------>")

    # write to csv file
    output_csv = "temp_output.csv"
    write_to_csv(df_houses, output_csv)
    print("finished")

    # create corr_matrix
    corr_matrix = df_houses.corr().abs()
    print(corr_matrix)

    # visualise correlations

    import matplotlib.pyplot as plt
    import seaborn as sns
    fig = plt.figure()
    sns.set_theme(style="whitegrid")
    sns.heatmap(corr_matrix, cmap="YlGnBu")
    fig.suptitle("correlations between price & other columns", fontsize=12)
    plt.title("correlations")
    plt.show()


if __name__ == '__main__':
    main()

"""
iterating over columns in a dataframe with iteritems

def print_unique_values(dframe):
    for column_name, column_data in dframe.iteritems():
        print(f"now on column: {column_name} \n")
        print(dframe[column_name].unique())

    
# print rows where price = 0.0
price_zeroes = df_houses[df_houses["price"] == 0]
print(price_zeroes)

"""
