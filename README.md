# ImmoAnalysis
With this repo we analyse the data of house sales in Belgium

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
$ conda create --name immograph python=3.9.5
$ conda activate immograph
```
### install conda packages
```
conda install pandas matplotlib seaborn
```

## read houses dataset in python:<br/>
```
houses = pd.read_csv("final_list_houses_dataset.csv", sep=',')
houses.head()
```
## configure your IDE to use Conda Environment
eg `~/anaconda3/envs/becode/bin/python

## Useful links for datacleaning
https://www.educative.io/edpresso/basic-data-cleaning-using-pandas

# data operations
## drop columns
"Unamed: 0"
## rename column
new column names
area price building_state facades bedrooms kitchen_equipped furnished open_fire locality land_surface terrace terrace_surface swimming_pool property_type property_subtype garden garden_surface
## fix type
property_subtype -> change value "exceptiona" to "exceptional"
## change dtype
### make categoricals for
kitchen_equipped building_state property_type property_subtype
### make bool
furnished swimming_pool garden terrace
### change dtype for
price->float64
facades->small int
bedrooms->small int
open_fire->small int
### NaN -> rounded(mean)
facades
bedrooms

## drop rows
check when price row it is not a float and then drop it

## check if there are any values not in datatype like with price

