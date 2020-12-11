from  geopy.distance import geodesic
import time
import copy

class Packet():

    def __init__(self, dist, dest):
        self.dist = dist
        self.dest = dest # destination zipcode

    def __lt__(self, other):
        return self.dist < other.dist

    def __eq__(self, other):
        if not isinstance(other, Packet):
            return False
        return (self.dist == other.dist)

    def __hash__(self, other):
        return hash((self.dist, self.dest))

class DistMatrix():

    def __init__(self):
        print("Beginning initialization of DistMatrix object...")
        start_time = time.time()
        self.mappings = dict()
        self.reverse_mappings = []

        f = open("ohio-zip-code-latitude-and-longitude.csv", 'r')
        lines = f.readlines()[1:]
        f.close()

        for i in range(len(lines)):
            tokens = lines[i].split(",")
            self.mappings[int(tokens[0])] = i
            self.reverse_mappings.append(int(tokens[0]))

        self.matrix = dict()
        for i in range(len(lines)):
            tokens1 = lines[i].split(",")
            zip1 = int(tokens1[0])
            lat1 = float(tokens1[3])
            long1 = float(tokens1[4])
            origin = (lat1, long1)
            self.matrix[zip1] = []

            for j in range(len(lines)):
                print("\tProgress: %.2f%%  \r" % (float(((len(self.mappings) * i) + j) * 100)/float(len(self.mappings) * len(self.mappings))), 
                    end='')
                tokens2 = lines[j].split(",")
                zip2 = int(tokens2[0])
                lat2 = float(tokens2[3])
                long2 = float(tokens2[4])
                dist = (lat2, long2)
                pkt = Packet(geodesic(origin, dist).miles, zip2)
                self.matrix[zip1].append(pkt)

        end_time = time.time()
        print("Finished initialization in %.2f seconds." % (end_time - start_time))

    def get_dist(self, zip1, zip2):
        if not zip1 in self.mappings.keys():
            raise Exception("Unknown location data for zip="+ str(zip1))

        if not zip2 in self.mappings.keys():
            raise Exception("Unknown location data for zip="+ str(zip2))

        return self.matrix[zip1][self.mappings[zip2]].dist

    def get_nearest(self, original_zip, num_neighbors, valid_zipcodes):
        neighbors = copy.deepcopy(self.matrix[original_zip])
        neighbors.sort()
        nearest_neighbors = [] 
        index = 0
        count = 0
        while (count < num_neighbors):
            if index == 0:
                index += 1
                continue
            zipCode = neighbors[index].dest
            if (zipCode in valid_zipcodes):
                nearest_neighbors.append(zipCode)
                count += 1
            index += 1
        return nearest_neighbors

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

class DistGrid():
    def __init__(self):
        f = open("ohio-zip-code-latitude-and-longitude.csv", 'r')
        lines = f.readlines()[1:]
        f.close()
        self.zipcodes = dict()
        self.reverse_mappings = dict()

        for i in range(len(lines)):
            tokens = lines[i].split(",")
            self.zipcodes[int(tokens[0])] = i
            self.reverse_mappings[i] = int(tokens[0])

        self.num_codes = len(self.zipcodes.keys())
        self.matrix = [[0.0 for _ in range(self.num_codes)] for _ in range(self.num_codes)]

        f = open("distances.csv", 'r')
        lines = f.readlines()[1:]
        f.close()

        for i in range(len(lines)):
            tokens = lines[i].split(",")
            z1 = int(tokens[0])
            z2 = int(tokens[1])
            dist = float(tokens[2])
            pkt = Packet(dist, z2)
            i1 = self.zipcodes[z1]
            i2 = self.zipcodes[z2]
            self.matrix[i1][i2] = pkt

    def get_dist(self, zip1, zip2):
        if not zip1 in self.zipcodes.keys():
            raise Exception("Unknown location data for zip="+ str(zip1))

        if not zip2 in self.zipcodes.keys():
            raise Exception("Unknown location data for zip="+ str(zip2))

        i1 = self.zipcodes[zip1]
        i2 = self.zipcodes[zip2]

        return self.matrix[i1][i2].dist

    def get_nearest(self, z0, num_neighbors, valid_zipcodes):
        i0 = self.zipcodes[z0]
        sorted_neighbors = copy.deepcopy(self.matrix[i0])
        sorted_neighbors.sort(key=lambda x: x.dist)
        sorted_neighbors = sorted_neighbors[1:]
        count = 0
        index = 0
        nearest_neighbors = []
        while (count < num_neighbors):
            pkt = sorted_neighbors[index]
            if not pkt.dest in valid_zipcodes:
                index += 1
                continue
            nearest_neighbors.append(pkt.dest)
            index += 1
            count += 1
        return nearest_neighbors

Distances = DistGrid()