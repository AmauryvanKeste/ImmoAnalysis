# ImmoAnalysis
With this repo we analyse the data of house sales in Belgium

## Useful links
https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html
https://www.educative.io/edpresso/basic-data-cleaning-using-pandas

## Project follow-up
Trello link : https://trello.com/invite/b/IAvi3eCo/00d69f2e66157cc2a033d9f7f9848b9f/immo-kanban

## to work on repo
git clone git@github.com:AmauryvanKeste/ImmoAnalysis.git

## setup conda environment
### select your python
```
conda search python
python                         3.9.4      hdb3f193_0  pkgs/main
python                         3.9.5      h12debd9_4  pkgs/main
python                         3.9.5      hdb3f193_3  pkgs/main
```
```
$ conda create --name immograph python=3.9
$ conda activate immograph
```
### install conda packages
```
conda install pandas matplotlib seaborn
```

## read houses dataset in python:<br/>
```
df_houses = pd.read_csv("final_list_houses_dataset.csv", sep=',')
df_houses.head()
```
## configure your IDE to use Conda Environment
eg `~/anaconda3/envs/becode/bin/python`


# data operations
## drop columns
"Unamed: 0"
## rename column
new column names:
* area
* price
* building_state
* facades
* bedrooms
* kitchen_equipped
* furnished
* open_fire
* locality
* land_surface
* terrace
* terrace_surface
* swimming_pool
* property_type
* property_subtype
* garden
* garden_surface

## fix typo
* property_subtype -> change
  * "exceptiona" to "exceptional"
## change dtype
### make categoricals for
* kitchen_equipped
  * 'installed'
  * nan -> 'undefined'
  * 'hyper equipped'
  * 'semi equipped'
  * 'usa semi equipped'
  * 'usa installed' 
  * 'usa hyper equipped'
  * 'not installed'
  * 'usa uninstalled'
* building_state
  * good
  * just renovated
  * as new
  * to renovate
  * to be done up
  * to restore
  * nan -> undefined
* property_type
  * 'house'
  * 'land'
  * 'other'
* property_subtype
  * 'house'
  * 'villa'µ
  * 'mixed'
  * 'town'
  * 'farmhouse'
  * 'chalet'
  * 'country'
  * 'exceptiona'
  * 'building'
  * 'apartment'
  * 'mansion'
  * 'bungalow'
  * 'other'
  * 'manor'
  * 'castle'
  * 'land'

### convert these columns to bool
* furnished
* swimming_pool
* garden
* terrace

### change dtype for
* price -> float64
* facades -> int8
* bedrooms -> int8
* open_fire -> int8

### NaN -> rounded(mean)
* facades
* bedrooms

## drop rows
check when price row is not a float and then drop it

## check if column has a value outside of datatype bounds like with price

