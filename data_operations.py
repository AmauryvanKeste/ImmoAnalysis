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

    # create a column with square prices
    df_houses['price_sq'] = round(df_houses['price'] / df_houses['area'], 0)

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

    # create bar plot for NaN averages
    sns.barplot(x=df_meaningful_nan.index, y='nans_percentage', data=df_meaningful_nan, palette=palette_blue)
    fig_barplot_nans.suptitle("NaN %/column before replacing NaN values with mean()/False", fontsize=9)
    plt.title("NaN percentage per column")

    # region data
    # a new column region is created based on following conditions
    # conditions for region
    brussels_region = df_houses['locality'].between(1000, 1299)
    wallonia_region = df_houses['locality'].between(1300, 1499) | df_houses['locality'].between(4000, 7999)
    flanders_region = df_houses['locality'].between(1500, 3999) | df_houses['locality'].between(8000, 9999)

    # create a region column & fill based on conditions
    conditions = [brussels_region, wallonia_region, flanders_region]
    choice = ["brussels", "wallonia", "flanders"]
    df_houses["region"] = np.select(conditions, choice)

    # calculate means of all numeric columns for every region
    # ('area', 'price', 'facades', 'bedrooms', 'furnished', 'open_fire', 'locality', 'land_surface')
    brussels_mean = df_houses[df_houses["region"] == "brussels"].mean()
    wallonia_mean = df_houses[df_houses["region"] == "wallonia"].mean()
    flanders_mean = df_houses[df_houses["region"] == "flanders"].mean()
    belgian_mean  = df_houses.mean()
    region_means = {"brussels": brussels_mean, 'wallonia': wallonia_mean, 'flanders': flanders_mean, 'belgium': belgian_mean}
    df_region_means = pd.DataFrame(region_means)
    mean_price_per_region = df_region_means.loc["price", df_region_means.columns]
    """
    brussels    1.320469e+06
    wallonia    3.632886e+05
    flanders    4.678083e+05
    belgium     4.828550e+05
    Name: price, dtype: float64
    """
    # PLOTTING SERIES DON'T DEFINE DATA=SOME_VAR this fix works for barplot but not for catplot
    x = list(mean_price_per_region.index)
    print(x)
    sns.catplot(
        data=mean_price_per_region,
        x=x,
        y=mean_price_per_region.values,  # values are the price float values
        kind="bar",
        palette=palette_blue
    )
    y_start, y_end, y_step = 0, 1400000, 100000
    plt.yticks(np.arange(y_start, y_end+y_step, y_step))
    plt.ylabel("price in euro * 1 million")
    plt.xlabel(x)

    # create and set an index for df_region_means dataframe
    # row_count = df_region_means.shape[0]  # same as len(df_region_means)
    # index_list = list(range(0, row_count))
    # df_region_means.index = index_list
    # df_region_means.set_index(inplace=True)

    # create square meter df
    belgium_sq_top5 = df_houses.groupby('locality').price_sq.mean().round().sort_values(ascending=False).head()

    # Chart Top 5 per square meter in Belgium
    plt.figure(figsize=(10, 5))
    plt.ylim(0, 100)  # range allowed on y-axis
    y_start, y_end, y_step = 0, 8000, 1000
    plt.yticks(np.arange(y_start, y_end + y_step, y_step))
    plt.title('Top 5 Prices per square meter in Belgium', color='black', fontsize=22)
    bel_sq_fig = sns.barplot(x=belgium_sq_top5.index, y=belgium_sq_top5.values,  palette='Blues_d')
    bel_sq_fig.set_ylabel('Price per square meter €')
    fig4 = bel_sq_fig.get_figure()
    fig4.savefig("prices_sq_m_belgium.png")

    bedrooms_price = sns.boxplot(y='bedrooms', x='price', data=df_houses, width=0.8, orient='h', showmeans=True,
                                 fliersize=3)
    plt.title('Price in function of number of bedrooms', color='black', fontsize=36)
    x_start, x_end, x_step = 0, 2000000, 100000
    plt.xticks(np.arange(x_start, x_end + x_step, x_step))
    fig8 = bedrooms_price.get_figure()
    fig8.savefig("bedrooms_price.png")

    fig, ax = plt.subplots(figsize=(12, 6))
    terrace_price = sns.boxplot(y='terrace', x='price', data=df_houses, width=0.8, orient='h', showmeans=True,
                                fliersize=3, ax=ax)
    plt.title('./Terrace and Price', color='black', fontsize=36)
    fig9 = terrace_price.get_figure()
    fig9.savefig("terrace_price.png")
    plt.show()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(y='building_state', x='price', data=df_houses, width=0.8, orient='h', showmeans=True, fliersize=3,
                ax=ax)
    plt.title('State and price', color='black', fontsize=36)
    fig10 = terrace_price.get_figure()
    fig10.savefig("state_price.png")

    plt.show()


if __name__ == '__main__':
    main()
