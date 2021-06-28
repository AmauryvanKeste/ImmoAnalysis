def initiate_pandas(max_rows=10, max_cols=10, console_width=640):
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


def set_dtype_col_to_bool(dframe, columns_list):
    for column in columns_list:
        dframe[column].astype('bool')


def replace_nan_in_column(dframe, columns_list, val):
    for column in columns_list:
        dframe[column].fillna(value=val, inplace=True)


def change_nan_value_to_mean(dframe, columns_list):
    for column in columns_list:
        mean = dframe[column].mean()
        print(mean)
        print("==========")


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
    rename_columns_dict(df_houses, d_rename_cols_old_new)
    cols_that_change_to_bool_dtype = ["swimming pool", "garden", "terrace", "furnished"]
    set_dtype_col_to_bool(df_houses, cols_that_change_to_bool_dtype)
    replace_nan_in_column(df_houses, "swimming pool", False)
    booleanate_these_columns = ["garden", "terrace"]
    change_zero_ones_to_true_false(df_houses, booleanate_these_columns)
    # replace "no" to "NaN" for price column
    replace_value_in_column(df_houses, "price", 'no', np.NaN)
    # need to set them to to mean() before casting
    change_nan_to_undefined = ["kitchen_equipped", "building_state"]
    for column in change_nan_to_undefined:
        replace_nan_in_column(df_houses, column, "undefined")

    kitchen_cat = ['installed', 'undefined', 'hyper equipped', 'semi equipped', 'usa semi equipped',
                   'usa installed', 'usa hyper equipped', 'not installed' 'usa uninstalled']
    building_state_cat = ['good', 'just renovated', 'as new', 'to renovate', 'to be done up', 'to restore',
                          'undefined']
    property_type_cat = ['house', 'land', 'other']
    property_subtype_cat = ['house', 'villa', 'mixed', 'town', 'farmhouse', 'chalet', 'country', 'exceptional',
                            'building', 'apartment', 'mansion', 'bungalow', 'other', 'manor', 'castle', 'land']


if __name__ == '__main__':
    main()

# def print_unique_values(dframe):
#     for column_name, column_data in dframe.iteritems():
#         print(f"now on column: {column_name} \n")
#         print(dframe[column_name].unique())
#         print(f"-------------------------------")
