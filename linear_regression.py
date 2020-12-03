import argparse
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_predict
from distances import Distances

FEATURES = ['cumulative',
            'last_30_days',
            'last_14_days',
            'per_100K_cumulative',
            'per_100K_last_30_days',
            'per_100K_last_14_days']



parser = argparse.ArgumentParser(description='Linear Regression on COVID data')
parser.add_argument('feature', metavar='F', type=str, 
                                                 help='The feature to predict')
parser.add_argument('neighbors', metavar='N', type=int,
                             help="Number of neighboring zipcodes to consider")
parser.add_argument('folds', metavar='K', type=int,
                      help="Number of folds to performs cross validation with")

args = parser.parse_args()
if (args.neighbors < 1):
    print("ERROR: Must specify at least 1 neighbor for consideration")
    exit()

if (not args.feature in FEATURES):
    print("Error: Feature must be one of "+ str(FEATURES))
    exit()

if (args.folds < 1):
    print("ERROR: Must specify at least 1 fold for cross validation")
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

print("Training linear regression model...", end='')
reg  = LinearRegression().fit(X, Y)
print("Success!")

# print(reg.score(X,Y))
# print(reg.coef_)
# print(reg.intercept_)

print("Beginning cross-validation...", end='')
y_pred = cross_val_predict(reg, X, Y, cv=args.folds)
print("Success!")

# print(y_pred)