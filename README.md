# COVID-19 Predictors in the State of Ohio 

This project was developed for the course CS-760: Machine Learning (Fall 2020).

Author: Ranganath (Bujji) Selagamsetty   
Author: Matthew Viens

## Dependencies

### GeoPy

This project uses GeoPy to compute the geodesic distance between two sets of longitude and lattitude coordinates. From the official [documentation](https://geopy.readthedocs.io/en/stable/), the `geodesic()` function returns the distance between two pairs of longitude and lattitude coordinates assuming the Earth's ellipsoidal shape.

### scikit-learn  

This project uses the `sklearn.linear_model.LinearRegression()` to create linear predictors for the COVID dataset `dataset.csv`. The official documentation can be found [here](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html).

## Running the Scripts

Running any of the following scripts will yield the error percentage as calculated by the model. This error 
is calculated by splitting the dataset usinge `train_test_split()` that uses 75% of the dataset as the training 
set and the remaining 25% as the validation set. For repeatability, the random seed of `7` is used during this process.

The error percentage is calculated and reported as:

Error Percentage = (1/N) * 100 * (y<sub>predicted</sub> - y<sub>actual</sub>) / y<sub>actual</sub>  

Where N is the number of samples in the test set. 

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

## Datasets

### distances.csv

The `distances.py` file created this file to write out the `distances.csv` file. The CSV has all the possible distances between pairs of ZIP codes in Ohio. 
The distances are calulated using GeoPy's `geodesic()` function. The `DistMatrix()` class worte out the raw distances to a file, but other source files 
can use the instantiated `DistGrid()` object `distances` for fast access to preprocessed distance information.

### dataset.csv

This file was created by the program `collate.py`. `collate.py` reads from the various CSVs to aggregate data per zipcode.  

### OH_COVIDSummaryDataZIP_11_29_20.csv

OH Covid Dataset: https://coronavirus.ohio.gov/wps/portal/gov/covid-19/dashboards/key-metrics/cases-by-zipcode  
    Retrieved 11/29/20  

### ohio_pop_by_city.csv

Ohio Population by City : https://www.ohio-demographics.com/cities_by_population  
    Retrieved 11/29/20  
    Manually scrapped from page  
    10 most populous entries manually augmented with county data from wikipedia, the rest given NaaC (Not Assigned a County) as their code  

### ohio_pop_by_zip_code.csv

Ohio Population by zipcode : https://www.ohio-demographics.com/zip_codes_by_population  
    Retrieved 11/29/20  
    Manually scraped from page due to lack of export  

### Population_By_County.csv

Ohio Population by Counties : https://www.ohio-demographics.com/counties_by_population  
    Retrieved 11/29/20  
    Manually scrapped from page  

### ohio_univerisities_information.csv

Ohio Universities : https://en.wikipedia.org/wiki/List_of_colleges_and_universities_in_Ohio#cite_note-5  
    Retrieved 11/29/20  
    Manually scrapped from page  
    Augmented with latitude/longitude & zip code data from Google Answers on google searching university name and "lat long"  
    County information from Wikipedia  

### us-zip-code-latitude-and-longitude.csv

US Zip Code Dataset: https://public.opendatasoft.com/explore/dataset/us-zip-code-latitude-and-longitude/table/  
    Retrieved 11/29/20

### ohio-zip-code-latitude-and-longitude.csv

This file is simply a subset of the `us-zip-code-latitude-and-longitude.csv` file, only recording the ZIP codes in Ohio.

### pop_density.csv 

Ohio Population Density Zip Code Rank: http://www.usa.com/rank/ohio-state--population-density--zip-code-rank.htm  
    Retrieved 12/1/2020  

### Extra Sources

Counties by zip code : https://www.zipcodestogo.com/Ohio/  
    Retrieved 11/29/20  
    Manually scraped from page

