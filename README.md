# CS_760_Ohio_COVID_Project

## Dependencies

### GeoPy

This project uses GeoPy to compute the geodesic distance between two sets of longitude and lattitude coordinates. From the official [documentation](https://geopy.readthedocs.io/en/stable/), the `geodesic()` function returns the distance between two pairs of longitude and lattitude coordinates assuming the Earth's ellipsoidal shape.

### scikit-learn  

## Running Linear Regression Simple

To run linear regression to predict a single COVID feature using on data in a 
given zipcode, use the following command:

`python linear_regression_simple.py -y LABEL -x FEATURES`

Some common examples are shown below: 

To run linear regression on cumulative number of COVID cases based on the number reported in the last 30 and last 14 days:  
`python linear_regression_simple.py -y 'cumulative' -x last_30_days last_14_days`


To run linear regression on cumulative rate of COVID cases based on the rates reported in the last 30 and last 14 days:  
`python linear_regression_simple.py -y 'per_100K_cumulative' -x per_100K_last_30_days per_100K_last_14_days`


## Running Linear Regression

To run the Linear Regression script, use the following command:

`python linear_regression.py "feature" num_neighbors num_folds`

Where "feature" must be one of: 

`
'cumulative'  
'last_30_days'  
'last_14_days'  
'per_100K_cumulative'  
'per_100K_last_30_days'  
'per_100K_last_14_days'  
`

num_neighbors specifies how many zipcodes to consider as neighboring

num_folds specifies the number of folds to use for cross validation

## Running Nearest Neighbors Regression

To run the Nearest Neighbors Regression, open the Inverse_Distance_Analysis.ipynb Jupyter Notebook.

Select from dropdown menus a Run All Cells option

All features are run simultaneously to improve efficency and the results will be exported as csv's due to the number of results compute.

Note that the results arrays are in terms of results[target_feature, distance_metric, neighbors_used].
This format carries through to the csv's which are results[:,:,k] for a value of k where the corresponding number of neighbors is noted in the file name.
All results are saved to the NN_Regression_Results file folder.
The transpose of these results are used in the written report where it is distance_metric by target feature for a fixed number of neighbors.
