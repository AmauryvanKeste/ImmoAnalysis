from dfops import DfOps
import numpy as np
import pandas as pd


def main():
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
    # read in all rows and all columns starting with the 2nd (1)
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',').iloc[:, 1:]
    immo_df_ops = DfOps(df_houses, 20, 15)

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
    immo_df_ops.rename_columns_dict(d_rename_cols_old_new)
    # todo: strip NaN's in facades, area, open_fire
    # set 1"s to True and 0's to False for following columns
    booleanize_these_columns = ["garden", "terrace"]
    immo_df_ops.change_zero_ones_to_true_false(booleanize_these_columns)

    # set no's to False and yes' to True for following columns
    yes_no_to_true_false = ["furnished", "swimming_pool"]
    immo_df_ops.change_no_yes_to_false_true(yes_no_to_true_false)

    # change dtype column to bool for following columns
    cols_that_change_to_bool_dtype = ["swimming_pool", "garden", "terrace", "furnished"]
    immo_df_ops.convert_cols_to_datatype(cols_that_change_to_bool_dtype, "bool")

    # change NaN to False for "swimming_pool" column
    immo_df_ops.replace_nan_in_column("swimming_pool", False)

    # count nans in rows
    percent_nan_values = df_houses.isna().sum() * 100 / len(df_houses)
    df_nan_values = pd.DataFrame({"nans_percentage": percent_nan_values})

    # replace "no" to "NaN" for price column
    immo_df_ops.replace_value_in_column("price", "no", np.NaN)

    # drop price rows that have NaN value
    indexes_price_is_no = df_houses[df_houses["price"].isna()].index
    df_houses.drop(indexes_price_is_no, inplace=True)

    # convert columns to float
    to_float_columns = ["facades", "bedrooms", "open_fire", "price"]
    immo_df_ops.convert_cols_to_datatype(to_float_columns, "float64")

    # replace NaN's for every column in list with value returned by get_mean_for_column()
    columns_to_mean = ["area", "facades", "bedrooms", "price", "open_fire"]
    for index, column in enumerate(columns_to_mean):
        immo_df_ops.apply_mean_to_column(column)

    # replace exception to exceptional
    immo_df_ops.replace_value_in_column("property_subtype", "exceptiona", "exceptional")

    # change NaN to "undefined" for following columns
    change_nan_to_undefined = ["kitchen_equipped", "building_state", "property_subtype"]
    immo_df_ops.replace_nan_in_column(change_nan_to_undefined, "undefined")

    # mixed dtypes conversion:
    #   df['col'] = pd.to_numeric(df['col'], errors='coerce')

    # create categoricals -> https://pandas.pydata.org/pandas-docs/stable/user_guide/categorical.html
    kitchen_equipped_cat = ['installed', 'undefined', 'hyper equipped', 'semi equipped', 'usa semi equipped',
                            'usa installed', 'usa hyper equipped', 'not installed', 'usa uninstalled']

    building_state_cat = ['good', 'just renovated', 'as new', 'to renovate', 'to be done up', 'to restore',
                          'undefined']
    property_type_cat = ['house', 'land', 'other']

    property_subtype_cat = ['house', 'villa', 'mixed', 'town', 'farmhouse', 'chalet',
                            'country', 'exceptional', 'building', 'apartment', 'mansion',
                            'bungalow', 'other', 'manor', 'castle', 'land', 'undefined']

    categories_column_d = {"kitchen_equipped": kitchen_equipped_cat,
                           "building_state": building_state_cat,
                           "property_type": property_type_cat,
                           "property_subtype": property_subtype_cat}

    # turn keys (columns) in categories_column_d dictionary into a Category
    for column, cat_list in categories_column_d.items():
        cat_type = immo_df_ops.create_category(cat_list)
        df_houses[column] = df_houses[column].astype(cat_type)


    immo_df_ops.print_datatypes()
    immo_df_ops.print_columns_has_nan_check()

    # write to csv file
    immo_df_ops.write_to_csv("temp_output.csv")

    # start visualisation

    # create corr_matrix
    corr_matrix = df_houses.corr().abs()

    # visualise correlations with a heatmap
    import matplotlib.pyplot as plt
    import seaborn as sns
    chart_style = "whitegrid"
    palette_blue = "Blues_d"
    colormap = sns.color_palette("Blues_d")

    fig_correlation_heatmap = plt.figure()  # figsize=(width, height)
    sns.set_theme(style=chart_style)
    sns.heatmap(corr_matrix, cmap=colormap)
    fig_correlation_heatmap.suptitle("correlations between price & other columns", fontsize=9)
    plt.title("correlations")

    # visualize NaN values/column before replacing them with a bar plot
    # df_meaningful_nan dataframe set after reading in csv
    fig_barplot_nans = plt.figure()
    sns.set_theme(style=chart_style)

    plt.ylim(0, 100)  # range allowed on y-axis
    y_start, y_end, y_step = 0, 100, 5
    plt.yticks(np.arange(y_start, y_end+y_step, y_step))
    # data = df with only columns that have percentages > 0
    df_meaningful_nan = df_nan_values[df_nan_values["nans_percentage"] > 0]

    sns.barplot(x=df_meaningful_nan.index, y='nans_percentage', data=df_meaningful_nan, palette=palette_blue)
    fig_barplot_nans.suptitle("NaN %/column before replacing NaN values with mean()/False", fontsize=9)
    plt.title("NaN percentage per column")

    # use show at end to display all plt.figure()'s
    plt.show()

    # Avg prices belgium df:
        # brussels = df_analysis.loc[(df_analysis['locality'] >= 1000) & (df_analysis['locality'] <= 1299), 'price']
        # wallonia = df_analysis.loc[((df_analysis['locality'] >= 1300) & (df_analysis['locality'] <= 1499)) | ((df_analysis['locality'] >= 4000) & (df_analysis['locality'] <= 7999)), 'price']
        # flanders = df_analysis.loc[((df_analysis['locality'] >= 1500) & (df_analysis['locality'] <= 3999)) | ((df_analysis['locality'] >= 8000) & (df_analysis['locality'] <= 9999)), 'price']
        # fl_mean = flanders.mean()
        # br_mean = brussels.mean()
        # wal_mean = wallonia.mean()
        # bel_mean = df_analysis['price'].mean()
        # regions = {'Region': ['Brussels', 'Wallonia', 'Flanders', 'Belgium'], 'Avg_Price': [br_mean, wal_mean, fl_mean, bel_mean]}
        # df_regions = pd.DataFrame(regions)
    # Avg prices Chart:
        plt.figure(figsize=(15,10))
        plt.ylim(0, 100)  # range allowed on y-axis
        y_start, y_end, y_step = 0, 2*1e6, 1e5
        plt.yticks(np.arange(y_start, y_end+y_step, y_step))
        plt.title('Average Prices in Belgium', color='black', fontsize=36)
        avg_fig = sns.barplot(x=df_regions.Region, y=df_regions.Avg_Price, data=df_regions, palette='Blues_d')
        avg_fig.set_ylabel('Average Price €')
        fig3 = avg_fig.get_figure()
        fig3.savefig("prices_avg_belgium.png")


if __name__ == '__main__':
    main()
