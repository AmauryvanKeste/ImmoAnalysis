def initiate_pandas(max_rows=20, max_cols=20, console_width=640):
    try:
        import pandas as pd_custom
        pd_custom.set_option('display.max_columns', max_cols)
        pd_custom.set_option('display.max_rows', max_rows)
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


def replace_nan_in_column(dframe, columns_list, new_val):
    for column in columns_list:
        dframe[column].fillna(value=new_val, inplace=True)
    print(dframe[columns_list[0]])


def convert_nan_to_datatype(dframe, columns_list, replace_nan_val, datatype):
    for column in columns_list:
        dframe[column] = dframe[column].fillna(replace_nan_val).astype(datatype)


def change_nan_value_to_mean(dframe, columns_list):
    for column in columns_list:
        mean = dframe[column].mean()
        print(mean)
        print("==========")


def cast_to_datatype(dframe, column_list, datatype):
    for column in column_list:
        dframe[column] = dframe[column].astype(datatype)


def category_builder(category_list):
    try:
        return pd.Series(category_list, dtype="category")
    except ValueError:
        print(f"something went wrong: {ValueError}")


def get_mean_for_column(dframe, column):
    if dframe[column].dtype == np.int8:
        # print(f"column {column}: {round(dframe[column].mean())}")
        return round(dframe[column].mean())
    elif dframe[column].dtype == float:
        # print(f"column {column}: {dframe[column].mean()}")
        return dframe[column].mean()


def write_to_csv(dframe, file_path):
    dframe.to_csv(file_path)


def main():
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
    # Because NaN is a float
    # a column of integers with even one missing values is cast to floating-point dtype
    # read in all rows and from col1 till last column
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',').iloc[:, 1:]
    # drop 'Unnamed: 0' column as use for it is unknown
    # df_houses.drop('Unnamed: 0', axis=1, inplace=True)
    # df_houses = pd.read_csv.iloc[:, 1:]
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
    cols_that_change_to_bool_dtype = ["swimming_pool", "garden", "terrace", "furnished"]
    cast_to_datatype(df_houses, cols_that_change_to_bool_dtype, "bool")

    # change NaN to False for "swimming_pool" column
    replace_nan_in_column(df_houses, ["swimming_pool"], False)

    # set 1"s to True and 0's to False for following columns
    booleanize_these_columns = ["garden", "terrace"]
    change_zero_ones_to_true_false(df_houses, booleanize_these_columns)

    # replace "no" to "NaN" for price column
    replace_value_in_column(df_houses, "price", 'no', np.NaN)

    # change NaN to "undefined" for following columns
    change_nan_to_undefined = ["kitchen_equipped", "building_state"]
    replace_nan_in_column(df_houses, change_nan_to_undefined, "undefined")

    # todo: this didn't work for building_state, kitchen_equipped, property_type, find reason

    # using pandas Int64 with capital I could also work
    # df['col'] = df['col'].astype('Int64')

    # cast to int8 datatype AND convert NaN values to 0
    convert_nan_to_datatype(df_houses, ["facades", "bedrooms", "open_fire"], 0, "int8")
    # cast to float datatype AND convert NaN values to 0.0
    convert_nan_to_datatype(df_houses, ["area", "price"], 0.0, "float64")

    # pd.to_numeric -> https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_numeric.html
    #   or astype() used here
    # mixed dtypes conversion:
    #   df['col'] = pd.to_numeric(df['col'], errors='coerce')
    # cast_to_datatype(df_houses, ["facades", "bedrooms", "open_fire"], "int8")
    # cast_to_datatype(df_houses, ["price"], "float64")

    # create categoricals -> https://pandas.pydata.org/pandas-docs/stable/user_guide/categorical.html
    kitchen_equipped_cat = ['installed', 'undefined', 'hyper equipped', 'semi equipped', 'usa semi equipped',
                            'usa installed', 'usa hyper equipped', 'not installed', 'usa uninstalled']
    building_state_cat = ['good', 'just renovated', 'as new', 'to renovate', 'to be done up', 'to restore',
                          'undefined']
    property_type_cat = ['house', 'land', 'other']
    property_subtype_cat = ['house', 'villa', 'mixed', 'town', 'farmhouse', 'chalet', 'country', 'exceptional',
                            'building', 'apartment', 'mansion', 'bungalow', 'other', 'manor', 'castle', 'land']

    categories_column_d = {"kitchen_equipped": kitchen_equipped_cat,
                           "building_state": building_state_cat,
                           "property_type": property_type_cat,
                           "property_subtype": property_subtype_cat}

    # turn every column into a pd.Series(Category)
    for column, cat_list in categories_column_d.items():
        df_houses[column] = category_builder(cat_list)

    # replace NaN's for every column in list with value returned by get_mean_for_column()
    columns_to_mean = ["facades", "bedrooms", "price", "open_fire"]
    for column in columns_to_mean:
        replace_nan_in_column(df_houses, columns_to_mean, get_mean_for_column(df_houses, column))
    """ means calculated:
    facades:   2.2822037257233454
    bedrooms:  3.595719381688466
    price:     481228.216706302
    open_fire: 0.08462148236226714
    """

    # print data types to check successful conversion
    print(df_houses.dtypes)

    # todo: thins go wrong starting wen double commas are encountered (row 7)
    # todo: do we have all columns before printing them out to csv?
    # todo: problem lies with building_state, property_type, they still have NaN values
    # 7,850.0,849000.0,,2,9,not installed,True,0,3300,615.0,True,20,True,,exceptional,False,0

    print(df_houses.head(20))
    # write to csv file to check more thoroughly
    output_csv = "temp_output.csv"
    write_to_csv(df_houses, output_csv)
    # todo: first multiple comma issue in output
    """
    6,256.0,210000.0,undefined,3,4,usa hyper equipped,True,0,7080,201.0,False,0,True,,country,False,0
    7,850.0,849000.0,,2,9,not installed,True,0,3300,615.0,True,20,True,,exceptional,False,0
    8,161.0,295500.0,,0,4,usa uninstalled,True,0,5590,533.0,False,0,True,,building,True,631
    9,61.0,42000.0,,0,1,,True,0,1460,194.0,False,0,True,,apartment,False,0
    10,160.0,229000.0,,2,3,,True,0,6230,480.0,True,10,True,,mansion,True,400
    """


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
