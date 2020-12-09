"""
The contents of this file uses the scikit Linear Regression tool to predict 
COVID related data based on data collected by zipcode.

@author Ranganath (Bujji) Selagamsetty
@author Matthew Viens
"""

import argparse
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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
parser.add_argument('-y', '--label', help='The feature to predict', 
    required=True)
parser.add_argument('-x', '--features',
    nargs='+',
    help="List of features to include in feature vector. Args must be \
        seperated by whitespace.",
    required=True)

args = parser.parse_args()
if not(args.label in FEATURES):
    print("ERROR: Must specify label as one of the following features:")
    print(FEATURES)
    exit()

for f in args.features:
    if f == args.label:
        print("ERRROR: Cannot use classification label as feature value!")
        exit()
    if not(f in FEATURES):
        print("ERROR: Can only use the following features:")
        print(FEATURES)
        print("You entered: '" + str(f) + "'")
        exit()

###############################################################################
#                          BEGIN DATA PROCESSING                              #
###############################################################################

# First, read in raw data
f = open("dataset.csv", 'r')
lines = f.readlines()[1:]
f.close()

"""
A lightweight class that associated COVID data to zipcode. Instantiations of 
this class can be placed into a set.
"""
class Data():

    def __init__(self, 
                 zipcode, 
                 population, 
                 cumulative, 
                 last_30_days,
                 last_14_days,
                 per_100K_cumulative, 
                 per_100K_last_30_days, 
                 per_100K_last_14_days, 
                 pop_den, 
                 num_universities,
                 num_students):
        self.zipcode = zipcode
        self.population = population
        self.case_count_cumulative = cumulative
        self.case_count_last_30_days = last_30_days
        self.case_count_last_14_days = last_14_days
        self.case_count_per_100K_cumulative = per_100K_cumulative
        self.case_count_per_100K_last_30_days = per_100K_last_30_days
        self.case_count_per_100K_last_14_days = per_100K_last_14_days
        self.pop_den = pop_den
        self.num_unis = num_universities
        self.students = num_students

    def __eq__ (self, other):
        if not isinstance(other, Data):
            return False

        return self.zipcode == other.zipcode

    def __hash__(self):
        return hash(self.zipcode)

    """
    Returns the list of data values that correspond to the features provided
    in _inclusions_. Values are ordered based on _inclusions_.
    """
    def toList(self, inclusions):
        result = []
        for inc in inclusions:
            if 'cumulative' == inc:
                result.append(self.case_count_cumulative)
            elif 'last_30_days' == inc:
                result.append(self.case_count_last_30_days)
            elif 'last_14_days' == inc:
                result.append(self.case_count_last_14_days)
            elif 'per_100K_cumulative' == inc:
                result.append(self.case_count_per_100K_cumulative)
            elif 'per_100K_last_30_days' == inc:
                result.append(self.case_count_per_100K_last_30_days)
            elif 'per_100K_last_14_days' == inc:
                result.append(self.case_count_per_100K_last_14_days)

        return result

# DATA pool used for fast access, indexed by zipcode
DATA = dict()
for i in range(len(lines)):
    tokens = lines[i].split(",")

    # if any of the COVID data is missing, skip
    if (tokens[0] == "None" or
        tokens[2] == "None" or
        tokens[3] == "None" or
        tokens[4] == "None" or
        tokens[5] == "None" or
        tokens[6] == "None" or
        tokens[7] == "None"):
        continue

    # Add data sample to the DATA pool
    DATA[int(tokens[0])] = Data(int(tokens[0]),   # zipcode
                                0,                # population
                                int(tokens[2]),   # cumulative
                                int(tokens[3]),   # last_30_days
                                int(tokens[4]),   # last_14_days
                                float(tokens[5]), # per_100K_cumulative
                                float(tokens[6]), # per_100K_last_30_days
                                float(tokens[7]), # per_100K_last_14_days
                                0,                # population density
                                0,                # num universities
                                0)                # num students

# Build feature and Label vectors
x = [] # Features
y = [] # Labels

# list of feature we want to look at
INCS = args.features 
# label must be first in the list
INCS.insert(0, args.label) 

for zipcode, data in DATA.items():
    row = data.toList(inclusions=INCS)
    y.append(row[0])
    x.append(row[1:])

X = np.array(x).reshape((len(DATA), len(x[0])))
Y = np.array(y).reshape((len(DATA), 1))

###############################################################################
#                                 VALIDATION                                  #
###############################################################################

X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    Y, 
                                                    test_size=0.25, 
                                                    random_state=7)
reg = LinearRegression().fit(X_train, y_train)
y_pred = np.array(reg.predict(X_test))

# Assess accuracy on test data
total = 0.0
for i in range(len(y_test)):
    difference = abs(y_pred[i][0] - y_test[i][0])
    error = float(difference) / float(abs(y_test[i][0]))
    total += 100.0 * error
avg_error = total / len(y_test)

print("Average error rate of: %.2f%%" % (avg_error))