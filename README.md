# Mathematical Models in Python #

This repository contains mathematical models :
- **Splines** : Consist of piecewise-defined polynomial functions that are smoothly connected at specific points, known as knots. Especially used in interpolation and curve fitting.

## Prerequisites ##

Before running this code, ensure you have the following :

- Python packages described in ***requirements.txt***.

## Input Dataset ##

The input dataset must be a table containing at least two columns of quantitative values.
The tolerated format in the script are multiple such as ***csv*** or ***xlsx***.

## Usage ##

### Splines ###

1. Navigate to the ***Splines*** directory containing the main script ***splines.py***.
```bash
cd Splines
```

2. Open the script ***splines.py*** and edit the input path in ***main*** function to target the desired dataset to use. Indicate also the column names of the interest variable X and Y. Additionally, the user can inform some parameters to configure the algorithm.
```python
if __name__ == "__main__" :
    input_path = 'Dataset/input_path'
    splines(input_path)
```

3. Run the script ***splines.py*** either in an IDE such as ***Spyder*** or in shell.
```bash
python3 splines.py
```
#### Example ####

By default, the script ***splines.py*** target an dataset example located in ***Dataset/spnbmd.csv***. Columns names of variables X and Y are respectively ***'age'*** and ***'spnbmd'***.
```python
if __name__ == "__main__" :
    input_path = 'Dataset/spnbmd.csv'
    splines(input_path)
```
```bash
python3 splines.py
```

## Results ##

The script display in shell the result in the spline computing. Additionnaly, the program save those score in the ***Output*** directory in a file named ***output.txt***. In this same ***Output*** directory the user will see the graphic of the variable distribution and the spline line computed in the file named ***graphic.png***.

## To do list ##

- [ ] Edit the data import by using pandas. Add names of X and Y columns in parameters in main. Handle the case of dataset in csv and excel.
- [ ] Adapt names of variables to make calculations easier to interpret. Refresh learning.
- [ ] Save scores in an output file in text format.
