import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import Toolkit
def print_unique_values(dframe):
    for column_name, column_data in dframe.iteritems():
        print(f"now on column: {column_name} \n")
        print(dframe[column_name].unique())
        print(f"-------------------------------")

def rename_columns_dict(dframe, d_newnames):
    dframe.rename(columns=d_newnames, inplace=True)

def load_pandas():
    # entries 10092
    pd = Toolkit.initiate_pandas(20, 20)
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',')
    df_houses.sort_index()
    # print_unique_values(df_houses)

    print("--------------------")
    print(df_houses.info())
    print("--------------------")
    # dtypes: float64(5), int64(6), object(7)
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
    rename_columns_dict(df_houses, d_rename_cols_old_new)
    """  null values
    Area m2                     1736
    state of the building       3116
    number of facades           2338
    number of bedrooms           152
    fully equipped kitchen      3423
    furnished                   3023
    open fire                   9346
    swimming pool               9692
    """
    print("=================")
    print(df_houses.info())

if __name__ == '__main__':
    load_pandas()