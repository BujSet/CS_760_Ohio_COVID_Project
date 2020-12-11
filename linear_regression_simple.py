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
            'per_100K_last_14_days',
            'population',
            'density',
            'universities',
            'students']

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
    required=False)
parser.add_argument('-a', '--all_features', help="Include all features.",
    action='store_true', required=False)

args = parser.parse_args()
if not(args.label in FEATURES):
    print("ERROR: Must specify label as one of the following features:")
    print(FEATURES)
    exit()

if not args.all_features:
    if len(args.features) == 0:
        print("ERROR: Must specify at least one feature to use!")
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
else:
    args.features = []
    for f in FEATURES:
        args.features.append(f)
    args.features.remove(args.label)
    assert(len(args.features) == len(FEATURES) - 1)

###############################################################################
#                          BEGIN DATA PROCESSING                              #
###############################################################################

# First, read in raw data
f = open("dataset.csv", 'r')
lines = f.readlines()[1:]
f.close()

"""
A lightweight class that associates COVID data to zipcode. Instantiations of 
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
            elif 'population' == inc:
                result.append(self.population)
            elif 'density' == inc:
                result.append(self.pop_den)
            elif 'universities' == inc:
                result.append(self.num_unis)
            elif 'students' == inc:
                result.append(self.students)

        assert(len(result) == len(inclusions))
        return result

# DATA pool used for fast access, indexed by zipcode
DATA = dict()
for i in range(len(lines)):
    tokens = lines[i].split(",")

    # if relevant data is missing skip
    if (tokens[0] == "None"):
        continue
    if (tokens[1] == "None" and 'population' in args.features):
        continue
    if  tokens[2] == "None" and 'cumulative' in args.features:
        continue 
    if tokens[3] == "None" and 'last_30_days' in args.features:
        continue
    if tokens[4] == "None" and 'last_14_days' in args.features:
        continue
    if tokens[5] == "None" and 'per_100K_cumulative' in args.features:
        continue
    if tokens[6] == "None" and 'per_100K_last_30_days' in args.features:
        continue
    if tokens[7] == "None" and 'per_100K_last_14_days' in args.features:
        continue

    is_important = [True for i in range(len(FEATURES) + 1)]

    # Determine whether we care about a certain features
    is_important[1] = 'population' in args.features or 'population' == args.label
    is_important[2] = 'cumulative' in args.features or 'cumulative' == args.label
    is_important[3] = 'last_30_days' in args.features or 'last_30_days' == args.label
    is_important[4] = 'last_14_days' in args.features or 'last_14_days' == args.label
    is_important[5] = 'per_100K_cumulative' in args.features or 'per_100K_cumulative' == args.label
    is_important[6] = 'per_100K_last_30_days' in args.features or 'per_100K_last_30_days' == args.label
    is_important[7] = 'per_100K_last_14_days' in args.features or 'per_100K_last_14_days' == args.label
    is_important[8] = 'density' in args.features or 'density' == args.label
    is_important[9] = 'universities' in args.features or 'universities' == args.label
    is_important[10] = 'students' in args.features or 'students' == args.label
    
    d_zipcode = int(tokens[0])

    # Treat missing entries in the dataset as 0 valued variables
    d_pop = int(tokens[1]) if is_important[1] else 0
    d_tot = int(tokens[2]) if is_important[2] else 0
    d_30  = int(tokens[3]) if is_important[3] else 0
    d_14  = int(tokens[4]) if is_important[4] else 0
    d_totr= float(tokens[5]) if is_important[5] else 0.0
    d_30r = float(tokens[6]) if is_important[6] else 0.0
    d_14r = float(tokens[7]) if is_important[7] else 0.0
    d_den = float(tokens[8]) if is_important[8] else 0.0
    d_uni = int(tokens[9]) if  is_important[9] else 0
    d_std = int(tokens[10]) if is_important[10] else 0 

    # Add data sample to the DATA pool
    DATA[d_zipcode] = Data(d_zipcode,   # zipcode
                           d_pop,       # population
                           d_tot,       # cumulative
                           d_30,        # last_30_days
                           d_14,        # last_14_days
                           d_totr,      # per_100K_cumulative
                           d_30r,       # per_100K_last_30_days
                           d_14r,       # per_100K_last_14_days
                           d_den,       # population density
                           d_uni,       # num universities
                           d_std)       # num students

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
    error = float(difference) / float(y_test[i][0])
    total += 100.0 * error
avg_error = total / len(y_test)

print("Average error rate of: %.2f%%" % (avg_error))