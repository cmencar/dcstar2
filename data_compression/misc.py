import matplotlib.pyplot as plt
import json


def scatterPlot(df, m_d, M_d):
    groups = df.groupby("classes")
    for name, group in groups:
        plt.plot(group["feature1"], group["feature2"], marker="o", linestyle="", label=name)

    plt.legend()
    plt.savefig('test_prototipi/banana/banana_new_100.png')


def create_json(m_d, M_d, prototypes):
    point_coordinates = prototypes[:, :-1].tolist()
    # print(point_coordinates)
    point_labels = prototypes[:, -1].tolist()
    # print(point_labels)
    point_id = list()
    for i in point_coordinates:
        point_id.append(point_coordinates.index(i))

    data = {'points': [], 'm_d': m_d, 'M_d': M_d}
    for i in range(len(point_coordinates)):
        coordinates = point_coordinates[i]
        data['points'].append({
            'coordinates': coordinates,
            'class': point_labels[i],
            'name': "point" + str(point_id[i] + 1)
        })

    with open("test_prototipi/banana/Json/banana_100.json", 'w') as output:
        json.dump(data, output, indent=1)
