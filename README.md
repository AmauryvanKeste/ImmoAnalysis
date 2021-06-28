# ImmoAnalysis
With this repo we analyse the data of house sales in Belgium

## Project follow-up
Trello link : https://trello.com/b/IAvi3eCo/immo-kanban

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
