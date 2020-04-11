from cut_sequences.point import Point
import random as rand
import json


# Class that defines a creator of a randomly generated set of points
class PrototypesCreator:

    # Method for creating a randomly generated list of points
    # and saving it in a JSON file
    # @filename: name and path directory of the file
    #  containing the information to be created
    # @n_points: number of points to be created
    # @n_classes: number of different classes to be used
    # @n_dimensions: number of search space dimensions, corresponding
    #  to the number of coordinates of the point
    # @m_d: smallest boundary cut of dimension d
    # @M_d: greatest boundary cut of dimension d
    def create(self, filename, n_points, n_classes, n_dimensions, m_d=0, M_d=1):

        # initialization of passed elements if them are invalids
        if n_points <= 0:
            n_points = 1
        if n_dimensions <= 0:
            n_dimensions = 2
        if n_classes <= 0:
            n_classes = 1
        if filename is None or filename == "":
            filename = "point_list.json"

        # definition of the list of points randomly.
        # The coordinates follow a particular distribution
        # of values (in this case the normal distribution)
        point_list = [ Point(coordinates = [rand.gauss((m_d+M_d)/2, (m_d+M_d)/5) for _ in range(n_dimensions)],
                             label = rand.randrange(1, n_classes + 1), name = "point_" + str(point_id+1))
                       for point_id in range(n_points) ]

        # definition of a dictionary where the points
        # information will be defined to be used to create
        # the json file containing them
        data = {'points': [], 'm_d': m_d, 'M_d': M_d}
        for point in point_list:
            coordinates = [ coordinate for coordinate in point.get_coordinates() ]
            data['points'].append({
                'coordinates' : coordinates,
                'class' : point.get_label(),
                'name' : point.get_name()
            })

        # creation of json file
        with open(filename, 'w') as output:
            json.dump(data, output)


    # Method for loading a list of points from a
    # particular JSON file
    # @filename: name and path directory of the file
    #  containing the information to be loaded
    def load(self, filename):

        # open the file and upload the file in it. The data
        # of the JSON file are acquired and saved in variables
        # that will then be passed as return value
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            m_d = data['m_d']
            M_d = data['M_d']
            point_list = [Point(coordinates=[ coordinate for coordinate in point['coordinates'] ], label=point['class'],
                                name=point['name']) for point in data['points']]

        # returning the loaded data
        return point_list, m_d, M_d

