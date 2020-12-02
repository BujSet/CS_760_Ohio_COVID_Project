from  geopy.distance import geodesic
import time

class DistMatrix():

    def __init__(self):
        print("Beginning initialization of DistMatrix object...")
        start_time = time.time()
        self.mappings = dict()

        f = open("ohio-zip-code-latitude-and-longitude.csv", 'r')
        lines = f.readlines()[1:]
        f.close()

        for i in range(len(lines)):
            tokens = lines[i].split(",")
            self.mappings[int(tokens[0])] = i

        mid_time = time.time()
        print("\tTook %.3f seconds to map zip codes to indices." % (mid_time - start_time))

        self.matrix = dict()
        for i in range(len(lines)):
            tokens1 = lines[i].split(",")
            zip1 = int(tokens1[0])
            lat1 = float(tokens1[3])
            long1 = float(tokens1[4])
            origin = (lat1, long1)
            self.matrix[zip1] = []
            print("\tProgress: %.2f%%  \r" % (float(i * 100)/float(len(self.mappings))), 
                end='')

            for j in range(len(lines)):
                tokens2 = lines[j].split(",")
                zip2 = int(tokens2[0])
                lat2 = float(tokens2[3])
                long2 = float(tokens2[4])
                dist = (lat2, long2)
                self.matrix[zip1].append(geodesic(origin, dist).miles)
        end_time = time.time()
        print("Finished initialization in %.3f seconds." % (end_time - start_time))

    def get_dist(self, zip1, zip2):
        if not zip1 in self.mappings.keys():
            raise Exception("Unknown location data for zip="+ str(zip1))

        if not zip2 in self.mappings.keys():
            raise Exception("Unknown location data for zip="+ str(zip2))

        return self.matrix[zip1][self.mappings[zip2]]

    def write_out(self):
        f = open("distances.csv", 'w')
        f.write("Zip1,Zip2,Distance(miles)\n")
        key_list = list(self.mappings.keys())
        val_list = list(self.mappings.values()) 
        for zip1 in self.matrix.keys():
            for j in range(len(self.mappings)):
                zip2 = key_list[val_list.index(j)]
                f.write(str(zip1)+","+str(zip2)+","+
                    str(self.matrix[zip1][self.mappings[zip2]])+"\n")
        f.close()

Distances = DistMatrix()