"""
The contents of this file uses the scikit Linear Regression tool to predict 
COVID related data based on data collected by zipcode. The program supports
using COVID data of neighboring zipcodes to predict on a COVID feature.

@author Ranganath (Bujji) Selagamsetty
@author Matthew Viens
"""

import argparse
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from distances import Distances

FEATURES = ['cumulative',
            'last_30_days',
            'last_14_days',
            'per_100K_cumulative',
            'per_100K_last_30_days',
            'per_100K_last_14_days']

###############################################################################
#                             INPUT VALIDATION                                #
###############################################################################

parser = argparse.ArgumentParser(description='Linear Regression on COVID data')
parser.add_argument('-F','--feature', type=str, 
                                                 help='The feature to predict')
parser.add_argument('-N', 'neighbors', type=int,
                             help="Number of neighboring zipcodes to consider")

args = parser.parse_args()
if (args.neighbors < 1):
    print("ERROR: Must specify at least 1 neighbor for consideration")
    exit()

if not (args.feature in FEATURES):
    print("Error: Feature must be one of "+ str(FEATURES))
    exit()

print("Reading raw data from dataset.csv..", end='')
# First, read in raw data
f = open("dataset.csv", 'r')
lines = f.readlines()[1:]
f.close()
print("Success!")

class Data():

    def __init__(self, zipcode, cumulative, last_30_days,last_14_days,
            per_100K_cumulative, per_100K_last_30_days, 
            per_100K_last_14_days):
        self.zipcode = zipcode
        self.case_count_cumulative = cumulative
        self.case_count_last_30_days = last_30_days
        self.case_count_last_14_days = last_14_days
        self.case_count_per_100K_cumulative = per_100K_cumulative
        self.case_count_per_100K_last_30_days = per_100K_last_30_days
        self.case_count_per_100K_last_14_days = per_100K_last_14_days

    def __eq__ (self, other):
        if not isinstance(other, Data):
            return False

        if (self.zipcode != other.zipcode):
            return False

        return True

    def __hash__(self):
        return hash(self.zipcode)

    def get(self, feature):
        global FEATURES

        if feature == FEATURES[0]:
            return self.case_count_cumulative
        elif feature == FEATURES[1]:
            return self.case_count_last_30_days
        elif feature == FEATURES[2]:
            return self.case_count_last_14_days
        elif feature == FEATURES[3]:
            return self.case_count_per_100K_cumulative
        elif feature == FEATURES[4]:
            return self.case_count_per_100K_last_30_days
        else:
            return self.case_count_per_100K_last_14_days

DATA = dict()
ZIPCODES = set()

for i in range(len(lines)):
    tokens = lines[i].split(",")
    if (tokens[0] == "None" or
        tokens[2] == "None" or
        tokens[3] == "None" or
        tokens[4] == "None" or
        tokens[5] == "None" or
        tokens[6] == "None" or
        tokens[7] == "None"):
        continue
    DATA[int(tokens[0])] = Data(int(tokens[0]),
                                int(tokens[2]),
                                int(tokens[3]),
                                int(tokens[4]),
                                float(tokens[5]),
                                float(tokens[6]),
                                float(tokens[7]))
    ZIPCODES.add(int(tokens[0]))

print("Building feature and label vectors...", end='')
order = []
x = []
y = []
for zipcode, data in DATA.items():
    order.append(zipcode)
    y.append(data.get(args.feature))
    nearest_neighbors = Distances.get_nearest(data.zipcode, args.neighbors, ZIPCODES)
    assert(len(nearest_neighbors) == args.neighbors)
    row = []
    for neighbor in nearest_neighbors:
        row.append(DATA[neighbor].get(args.feature))
    x.append(row)

X = np.array(x).reshape((len(DATA), args.neighbors))
Y = np.array(y).reshape((len(DATA), 1))
print("Success!")

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=7)
reg = LinearRegression().fit(X_train, y_train)
y_pred = np.array(reg.predict(X_test))
assert(len(y_test) == len(y_pred))
total = 0.0
for i in range(len(y_test)):
    total += (100.0 * (y_pred[i][0] - y_test[i][0])) / y_test[i][0]
avg_error = total / len(y_test)

print("Average error rate of: %.2f%%" % (avg_error))