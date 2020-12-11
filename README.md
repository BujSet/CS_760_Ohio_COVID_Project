# CS_760_Ohio_COVID_Project

## Dependencies

### GeoPy

This project uses GeoPy to compute the geodesic distance between two sets of longitude and lattitude coordinates. From the official [documentation](https://geopy.readthedocs.io/en/stable/), the `geodesic()` function returns the distance between two pairs of longitude and lattitude coordinates assuming the Earth's ellipsoidal shape.

### scikit-learn  

## Running the Scripts

Running any of the following scripts will yield the error percentage as calculated by the model. This error 
is calculated by splitting the dataset usinge `train_test_split()` that uses 75% of the dataset as the training 
set and the remaining 25% as the validation set. For repeatability, the random seed of `7` is used during this process.

The error percentage is calculated and reported as:

Error Percentage = 100 * (y<sub>predicted</sub> - y<sub>actual</sub>) / y<sub>actual</sub>

### Running Linear Regression Simple

Below is a list of available ZIP code specific features that can be used with this script:

| Features | Description |
| -------- | ----------- |
| cumulative | Cumulative Absolute Occurrence |
| last_14_days | 14 Day Absolute Occurrence |
| last_30_days | 30 Day Absolute Occurrence |
| per_100K_cumulative | Cumulative Per 100K Occurrence Rate |
| per_100K_last_14_days | 14 Day Per 100K Occurrence Rate |
| per_100K_last_30_days | 30 Day Per 100K Occurrence Rate |
| population | Population |
| density | Population Density (Population per Square Mile) |
| universities | Number of Universities |
| students | Total Number of University Students |

To run linear regression to predict a single COVID feature using only some of the COVID features in a 
given zipcode, use the following command:

`python linear_regression_simple.py -y LABEL -x FEATURES`

Where _LABEL_ is the feature you want to predict, and _FEATURES_ is a white-space separated list of features to build the feature matrix.

To run linear regression on cumulative number of COVID cases based on the number reported in the last 30 and last 14 days:  
`python linear_regression_simple.py -y 'cumulative' -x last_30_days last_14_days`

To run linear regression on cumulative rate of COVID cases based on the rates reported in the last 30 and last 14 days:  
`python linear_regression_simple.py -y 'per_100K_cumulative' -x per_100K_last_30_days per_100K_last_14_days`

The following command can be used to predict on a specific label with all of the possible features:
`python linear_regression_simply.py -y LABEL -a`


### Running Linear Regression Nearest Neighbors

Below is a list of available ZIP code specific features that can be used with this script:

| Features | Description |
| -------- | ----------- |
| cumulative | Cumulative Absolute Occurrence |
| last_14_days | 14 Day Absolute Occurrence |
| last_30_days | 30 Day Absolute Occurrence |
| per_100K_cumulative | Cumulative Per 100K Occurrence Rate |
| per_100K_last_14_days | 14 Day Per 100K Occurrence Rate |
| per_100K_last_30_days | 30 Day Per 100K Occurrence Rate |


To run the Linear Regression Nearest Neighbors script, use the following command:

`python linear_regression_neighbors.py -f LABEL -n NUM_NEIGHBORS`

The usage is similar to `linear_regression_simple.py`.

### Running Nearest Neighbors Regression

To run the Nearest Neighbors Regression, open the Inverse_Distance_Analysis.ipynb Jupyter Notebook.

Select from dropdown menus a Run All Cells option

All features are run simultaneously to improve efficency and the results will be exported as csv's due to the number of results compute.

Note that the results arrays are in terms of results[target_feature, distance_metric, neighbors_used].
This format carries through to the csv's which are results[:,:,k] for a value of k where the corresponding number of neighbors is noted in the file name.
All results are saved to the NN_Regression_Results file folder.
The transpose of these results are used in the written report where it is distance_metric by target feature for a fixed number of neighbors.
