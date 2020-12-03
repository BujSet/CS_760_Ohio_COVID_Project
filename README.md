# CS_760_Ohio_COVID_Project

## Dependencies
geopy  

## Running Linear Regression

To run the Linear Regression script, use the followign command:

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
