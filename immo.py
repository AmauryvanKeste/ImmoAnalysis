import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import Toolkit

def load_pandas():
    # entries 10092
    df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',')
    df_houses.sort_index()
    """['house' 'villa' 'mixed' 'town' 'farmhouse' 'chalet' 'country'
    'exceptiona' 'building' 'apartment' 'mansion' 'bungalow' 'other' 'manor'
    'castle' 'land']"""
    print(df_houses['fully equipped kitchen'].unique())
    """
    ['installed' nan 'hyper equipped' 'semi equipped' 'usa semi equipped'
     'usa installed' 'usa hyper equipped' 'not installed' 'usa uninstalled']"""
    # drop
    print(df_houses.head(20))
    print(df_houses.describe())
    print("--------------------")
    print(df_houses.info())
    print("--------------------")
    print(df_houses.isnull().sum())
    # dtypes: float64(5), int64(6), object(7)
    """
    price -> float64
    state building -> ['good' 'just renovated' 'as new' 'to renovate' nan 'to be done up' 'to restore'] 
    furnished -> to bool
    
    """
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
    pd = Toolkit.initiate_pandas(20, 20)
    load_pandas()