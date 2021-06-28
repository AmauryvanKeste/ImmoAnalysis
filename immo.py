import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import Toolkit
def print_unique_values(dframe):
    for column_name, column_data in dframe.iteritems():
        print(f"now on column: {column_name} \n")
        print(dframe[column_name].unique())
        print(f"-------------------------------")

def load_pandas():
    # entries 10092
    pd = Toolkit.initiate_pandas(20, 20)
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',')
    df_houses.sort_index()
    print_unique_values(df_houses)

    print("--------------------")
    print(df_houses.info())
    print("--------------------")
    # dtypes: float64(5), int64(6), object(7)
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

if __name__ == '__main__':
    load_pandas()