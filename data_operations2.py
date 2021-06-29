import numpy as np
import pandas as pd
# drop column --> 'Unnamed: 0
    #df_houses.drop('Unnamed: 0', axis=1, inplace=True)
def initiate_pandas(max_rows=10, max_cols=10, console_width=640):
    try:
        import pandas as pd
        pd.set_option('display.max_columns', max_cols)
        pd.set_option('display.max_rows', max_rows)
        pd.set_option('display.width', console_width)  # make output in console wider
        return pd
    except ImportError:
        print("pandas not installed")

# rename columns:
def print_unique_values(dframe):
    for column_name, column_data in dframe.iteritems():
        print(f"now on column: {column_name} \n")
        print(dframe[column_name].unique())
        print(f"-------------------------------")

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


# def convert_col_to_categorical(dframe, column, cat_list):
#     pd.DataFrame({column}: cat_list)


def main():
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',')
    # sorting out of habit for performance
    df_houses.sort_index()
    # drop 'Unnamed: 0' column as use for it is unknown
    df_houses.drop('Unnamed: 0', axis=1, inplace=True)
    d_rename_cols_old_new = {"Area [m²]": "area"
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
    # renaming columns for ease of use
    rename_columns_dict(df_houses, d_rename_cols_old_new)

    # convert following columns to dtype bool
    cols_that_change_to_bool_dtype = ["swimming_pool", "garden", "terrace", "furnished"]
    set_dtype_col_to_bool(df_houses, cols_that_change_to_bool_dtype)

    # replace NaN values to False for "swimming_pool" column
    replace_nan_in_column(df_houses, ["swimming_pool"], False)

    # 0's to False and 1's to True
    booleanate_these_columns = ["garden", "terrace"]
    change_zero_ones_to_true_false(df_houses, booleanate_these_columns)

    # replace "no" to "NaN" for price column
    replace_value_in_column(df_houses, "price", 'no', np.NaN)

    # set every NaN value to mean for these columns:
    columns_to_mean = ["facades", "bedrooms", "price", "open_fire"]
    change_nan_value_to_mean(df_houses, columns_to_mean)

    # change NaN to "undefined" for following columns:
    nan_to_undefined_columns = ["kitchen_equipped", "building_state"]
    replace_nan_in_column(df_houses, nan_to_undefined_columns, "undefined")

    # start category creation
    kitchen_cat = ['installed', 'undefined', 'hyper equipped', 'semi equipped', 'usa semi equipped',
                        'usa installed', 'usa hyper equipped', 'not installed' 'usa uninstalled']
    building_state_cat = ['good', 'just renovated', 'as new', 'to renovate', 'to be done up', 'to restore',
                       'undefined']
    property_type_cat = ['house', 'land', 'other' ]
    property_subtype_cat = ['house', 'villa', 'mixed', 'town', 'farmhouse', 'chalet', 'country', 'exceptional',
                            'building', 'apartment', 'mansion', 'bungalow', 'other', 'manor', 'castle', 'land']


if __name__ == '__main__':
    main()


# Price column:
    # Drop all 'no' elements
        # indexNames = df_houses[df_houses['price'] == 'no' ].index
        # df_houses.drop(indexNames, inplace=True)
    # Convert colimn dtype to float64
        #df_houses.price = df_houses.price.astype('float64')
    # Calculate mean price
        # df_houses.price.mean()

