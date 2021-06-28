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


def change_value_in_column(dframe, column, old_value, new_value):
    dframe[column] = dframe[column].replace(to_replace=old_value, value=new_value)


def main():
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',')
    df_houses.sort_index()
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
    change_value_in_column(df_houses, selected_column="property_subtype", old_val="exceptiona", new_val="exceptional")


if __name__ == '__main__':
    main()

# dtype changes + NaN values fill
    #swimming_pool:
    # df_houses['swimming_pool'].fillna(value=False, inplace=True)
    # df_houses.astype({'swimming_pool': 'bool'}).dtypes

    #garden:
    # df_houses['garden'] = df_houses['garden'].replace(to_replace=0, value=False)
    # df_houses['garden'] = df_houses['garden'].replace(to_replace=1, value=True)
    # df_houses['garden'] = df_houses['garden'].replace(to_replace=1, value=True)

    #terrace:
    # df_houses['terrace'] = df_houses['terrace'].replace(to_replace=0, value=False)
    # df_houses['terrace'] = df_houses['terrace'].replace(to_replace=1, value=True)
    # df_houses.astype({'terrace': 'bool'}).dtypes
    
