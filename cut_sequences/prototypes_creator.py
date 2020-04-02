from cut_sequences.point import Point
import random as rand
import json


class PrototypesLoader:

    def load(self, filename):

        m_d = None
        M_d = None
        point_list = None

        with open(filename) as json_file:

            data = json.load(json_file)
            m_d = data['m_d']
            M_d = data['M_d']
            point_list = [Point(coordinates=[ coordinate for coordinate in point['coordinates'] ], label=point['class'],
                                name=point['name']) for point in data['points']]

        return point_list, m_d, M_d




class PrototypesCreator:

    def create(self, filename, n_points, n_classes, n_dimensions, m_d=0, M_d=1):

        if n_points <= 0:
            n_points = 1
        if n_dimensions <= 0:
            n_dimensions = 2
        if n_classes <= 0:
            n_classes = 1
        if filename is None or filename == "":
            filename = "point_list.json"

        point_list = [ Point(coordinates=[rand.gauss((m_d+M_d)/2, (m_d+M_d)/4) for _ in range(n_dimensions)],
                             label=rand.randrange(1, n_classes + 1), name="point_" + str(point_id+1)) for point_id in range(n_points) ]

        data = {'points': [], 'm_d': m_d, 'M_d': M_d}
        for point in point_list:
            coordinates = [ coordinate for coordinate in point.get_coordinates() ]
            data['points'].append({
                'coordinates' : coordinates,
                'class' : point.get_label(),
                'name' : point.get_name()
            })

        with open(filename, 'w') as output:
            json.dump(data, output)
