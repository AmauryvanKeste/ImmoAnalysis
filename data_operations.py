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


def main():
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',')
    df_houses.sort_index()
    df_houses.drop('Unnamed: 0', axis=1, inplace=True)
    d_rename_cols_old_new = {
        "Area [m²]": "area"
        , "Price [€]": "price"
        , "state of the building": "building_state"
        , "number of facades": "facades"
        , "number of bedrooms": "bedrooms"
        , "fully equipped kitchen": "kitchen_equipped"
        , "open fire": "open_fire"
        , "locality [zip code]": "locality"
        , "surface of the land [m²]": "land_surface"
        , "terrace surface [m²]": "terrace_surface"
        , "swimming pool": "swimming_pool"
        , "type of property": "property_type"
        , "subtype of property": "property_subtype"
        , "garden surface [m²]": "garden_surface"
    }
    # renaming columns
    rename_columns_dict(df_houses, d_rename_cols_old_new)

    # converting columns to dtype bool
    cols_that_change_to_bool_dtype = ["swimming_pool", "garden", "terrace", "furnished"]
    cast_to_datatype(df_houses, cols_that_change_to_bool_dtype, "bool")

    # change nan to False for swimming pool column
    replace_nan_in_column(df_houses, ["swimming_pool"], False)

    # 1 -> True and 0 -> False for garden & terrace columns
    booleanize_these_columns = ["garden", "terrace"]
    change_zero_ones_to_true_false(df_houses, booleanize_these_columns)

    # replace "no" to "NaN" for price column
    replace_value_in_column(df_houses, "price", 'no', np.NaN)

    # change NaN to "undefined" for following columns
    change_nan_to_undefined = ["kitchen_equipped", "building_state"]
    replace_nan_in_column(df_houses, change_nan_to_undefined, "undefined")

    # cast to int8, float64 before calculating mean
    # ValueError: Cannot convert non-finite values (NA or inf) to integer
    # changing NaN to 0 and 0.0 first resolves casting issue
    # using pandas Int64 with capital I could also work
    # df['col'] = df['col'].astype('Int64')

    # replace_nan_in_column(df_houses,["facades", "bedrooms", "open_fire"], 0)
    convert_nan_to_datatype(df_houses, ["facades", "bedrooms", "open_fire"], 0, "int8")
    # replace_nan_in_column(df_houses,["price"], 0.0)
    convert_nan_to_datatype(df_houses, ["price"], 0.0, "float")
    # todo: area column has NaN values, replace those

    # pd.to_numeric -> https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_numeric.html
    #   or astype() used here
    # mixed dtypes conversion:
    #   df['col'] = pd.to_numeric(df['col'], errors='coerce')
    cast_to_datatype(df_houses, ["facades", "bedrooms", "open_fire"], "int8")
    cast_to_datatype(df_houses, ["price"], "float64")

    # change nan values to mean() value for following columns
    columns_to_mean = ["facades", "bedrooms", "price", "open_fire"]
    # change_nan_value_to_mean(df_houses, columns_to_mean)
    # todo: apply mean values
    mean_price =  df_houses["price"].mean()
    print(mean_price)

    # print rows where price = 0.0
    price_zeroes = df_houses[df_houses["price"] == 0]
    print(price_zeroes)

    # create categoricals -> https://pandas.pydata.org/pandas-docs/stable/user_guide/categorical.html
    kitchen_equipped_cat = ['installed', 'undefined', 'hyper equipped', 'semi equipped', 'usa semi equipped',
                   'usa installed', 'usa hyper equipped', 'not installed', 'usa uninstalled']
    building_state_cat = ['good', 'just renovated', 'as new', 'to renovate', 'to be done up', 'to restore',
                          'undefined']
    property_type_cat = ['house', 'land', 'other']
    property_subtype_cat = ['house', 'villa', 'mixed', 'town', 'farmhouse', 'chalet', 'country', 'exceptional',
                            'building', 'apartment', 'mansion', 'bungalow', 'other', 'manor', 'castle', 'land']

    categories_column_d = { "kitchen_equipped": kitchen_equipped_cat ,
                            "building_state": building_state_cat,
                            "property_type": property_type_cat,
                            "property_subtype": property_subtype_cat}

    # turn every column into a pd.Series(Category)
    for column, cat_list in categories_column_d.items():
        df_houses[column] = category_builder(cat_list)

    # print data types to check successful conversion
    print(df_houses.dtypes)


if __name__ == '__main__':
    main()

# def print_unique_values(dframe):
#     for column_name, column_data in dframe.iteritems():
#         print(f"now on column: {column_name} \n")
#         print(dframe[column_name].unique())
#         print(f"-------------------------------")
