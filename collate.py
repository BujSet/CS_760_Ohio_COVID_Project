"""
The contents of this file implement a program that reads through very
specific files to collate zip code toa single output dataset. This program 
has already been run to create an comprehensive dataset, so there is not need
for it to be run again.

@author: Ranganath (Bujji) Selagamsetty
@author: Matthew Viens
"""

# List of files to read from
files = ["counties_by_zip_code.csv",
         "OH_COVIDSummaryDataZIP_11_29_20.csv",
         "ohio_pop_by_city.csv",
         "ohio_pop_by_zip_code.csv",
         "ohio_univerisities_information.csv",
         "Population_By_County.csv",
         "us-zip-code-latitude-and-longitude.csv"]

"""
Simple class to associate parsed data with zipcodes
"""
class Data:
    def __init__(self):
        self.zip_code = None
        self.city = None
        self.county = None
        self.population = None
        self.case_count_cumulative = None
        self.case_count_last_30_days = None
        self.case_count_last_14_days = None   
        self.case_count_per_100K_cumulative = None   
        self.case_count_per_100K_last_30_days = None
        self.case_count_per_100K_last_14_days = None
        self.population_density = None
        self.num_universities = 0
        self.num_uni_students = 0

    def __eq__ (self, other):
        if not isinstance(other, Data):
            return False

        if (self.zip_code != other.zip_code):
            return False

        return True

    def __hash__(self):
        return hash(self.zip_code)

    """
    Returns a list of all collected features from a data sample 
    """
    def toList(self):
        result = []
        result.append(self.zip_code)
        result.append(self.city)
        result.append(self.county)
        result.append(self.population)
        result.append(self.case_count_cumulative)
        result.append(self.case_count_last_30_days)
        result.append(self.case_count_last_14_days)   
        result.append(self.case_count_per_100K_cumulative)   
        result.append(self.case_count_per_100K_last_30_days)
        result.append(self.case_count_per_100K_last_14_days)
        result.append(self.population_density)
        result.append(self.num_universities)
        result.append(self.num_uni_students)
        return result

    """
    Used to create a CSV
    """
    def __str__(self):
        string = ""
        string += str(self.zip_code) + ","
        string += str(self.population) + ","
        string += str(self.case_count_cumulative) + ","
        string += str(self.case_count_last_30_days) + ","
        string += str(self.case_count_last_14_days) + ","
        string += str(self.case_count_per_100K_cumulative) + ","   
        string += str(self.case_count_per_100K_last_30_days) + ","
        string += str(self.case_count_per_100K_last_14_days) + ","
        string += str(self.population_density) + ","
        string += str(self.num_universities) + ","
        string += str(self.num_uni_students)
        return string


dataset = dict()

###############################################################################
#                             PARSE THROUGH FILE 1                            #
###############################################################################

f = open("counties_by_zip_code.csv", 'r')
lines = f.readlines()
f.close()

for i in range(len(lines)):
    if i == 0:
        continue
    data_point = Data()
    tokens = lines[i].split(",")
    assert(len(tokens) == 3)
    data_point.zip_code = int(tokens[0])
    data_point.city = tokens[1].strip()
    data_point.county = tokens[2].strip()
    dataset[data_point.zip_code] = data_point

###############################################################################
#                             PARSE THROUGH FILE 2                            #
###############################################################################

f = open("OH_COVIDSummaryDataZIP_11_29_20.csv", 'r')
lines = f.readlines()
f.close()
writeLines = []

for i in range(len(lines)):
    if (i == 0):
        writeLines.append(lines[0])
        continue
    str_row = ""
    in_quotes = False
    for c in lines[i]:
        if c == '"' and not in_quotes:
            in_quotes = True
            continue
        elif c == '"' and in_quotes:
            in_quotes = False
            continue
        elif c == ',' and in_quotes:
            continue
        else:
            str_row += c
    writeLines.append(str_row)

# Rewrite data file to remove pesky characters
f = open("OH_COVIDSummaryDataZIP_11_29_20___1.csv", 'w')
lines = f.writelines(writeLines)
f.close()

f = open("OH_COVIDSummaryDataZIP_11_29_20___1.csv", 'r')
lines = f.readlines()
f.close()

"""
Simple helper function to convert a string to the right data type
"""
def convert(string):
    if string.strip() == "N/A":
        return None
    elif '.' in string:
        return float(string)
    else:
        return int(string)


for i in range(len(lines)):
    if i == 0:
        continue
    tokens = lines[i].split(",")
    assert(len(tokens) == 8)
    zip_code = int(tokens[0])
    if zip_code in dataset:
        dataset[zip_code].population = convert(tokens[1])
        dataset[zip_code].case_count_cumulative = convert(tokens[2])
        dataset[zip_code].case_count_last_30_days = convert(tokens[3])
        dataset[zip_code].case_count_last_14_days = convert(tokens[4])
        dataset[zip_code].case_count_per_100K_cumulative = convert(tokens[5])   
        dataset[zip_code].case_count_per_100K_last_30_days =  convert(tokens[6])
        dataset[zip_code].case_count_per_100K_last_14_days =  convert(tokens[7])
    else:
        data_point = Data()
        data_point.zip_code = zip_code
        data_point.city = None
        data_point.county = None
        data_point.population = convert(tokens[1])
        data_point.case_count_cumulative = convert(tokens[2])
        data_point.case_count_last_30_days = convert(tokens[3])
        datas_point.case_count_last_14_days = convert(tokens[4])
        datas_point.case_count_per_100K_cumulative = convert(tokens[5])   
        datas_point.case_count_per_100K_last_30_days =  convert(tokens[6])
        datas_point.case_count_per_100K_last_14_days =  convert(tokens[7])
        dataset[zip_code] = data_point

###############################################################################
#                             PARSE THROUGH FILE 3                            #
###############################################################################

f = open("pop_density.csv", 'r')
lines = f.readlines()
f.close()

for i in range(len(lines)):
    if i == 0:
        continue
    tokens = lines[i].split(",")
    pop_den = float(tokens[0].strip())
    zip_code = int(tokens[1].strip())
    if zip_code in dataset:
        dataset[zip_code].population_density = pop_den
    else:
        data_point = Data()
        data_point.zip_code = zip_code
        data_point.city = None
        data_point.county = None
        data_point.population = None
        data_point.case_count_cumulative = None
        data_point.case_count_last_30_days = None
        datas_point.case_count_last_14_days = None
        datas_point.case_count_per_100K_cumulative = None   
        datas_point.case_count_per_100K_last_30_days = None
        datas_point.case_count_per_100K_last_14_days = None
        data_point.population_density = pop_den
        dataset[zip_code] = data_point

###############################################################################
#                             PARSE THROUGH FILE 4                            #
###############################################################################

f = open("ohio_univerisities_information.csv", 'r')
lines = f.readlines()
f.close()

for i in range(len(lines)):
    if i == 0:
        continue
    tokens = lines[i].split(",")
    zip_code = int(tokens[0])
    students = int(tokens[1])
    if zip_code in dataset:
        dataset[zip_code].num_universities += 1
        dataset[zip_code].num_uni_students += students
    else:
        data_point = Data()
        data_point.zip_code = zip_code
        data_point.city = None
        data_point.county = None
        data_point.population = None
        data_point.case_count_cumulative = None
        data_point.case_count_last_30_days = None
        datas_point.case_count_last_14_days = None
        datas_point.case_count_per_100K_cumulative = None   
        datas_point.case_count_per_100K_last_30_days = None
        datas_point.case_count_per_100K_last_14_days = None
        data_point.population_density = None
        data_point.num_universities = 1
        data_point.num_uni_students = students
        dataset[zip_code] = data_point

###############################################################################
#                        PUTPUT THE COLLATED DATASET                          #
###############################################################################


count = 0
for k,v in dataset.items():
    if not ("None" in str(v)):
        count += 1
    print(v)

print(count)
print(len(dataset))

# Zip Code, Population, case_count_cumulative, case_count_last_30_days,case_count_last_14_days,case_count_per_100K_cumulative,case_count_per_100K_last_30_days,case_count_per_100K_last_14_days
f = open("dataset.csv", 'w')
f.write("ZipCode,Population,case_count_cumulative,case_count_last_30_days,case_count_last_14_days,case_count_per_100K_cumulative,case_count_per_100K_last_30_days,case_count_per_100K_last_14_days,population_density,num_universities,num_uni_students\n")
for k,v in dataset.items():
    f.write(str(v) + "\n")
f.close()