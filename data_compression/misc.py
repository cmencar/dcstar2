import matplotlib.pyplot as plt
import json


def scatterPlot(df, alpha):
    groups = df.groupby("species")
    for name, group in groups:
        plt.plot(group["f1"], group["f2"], marker="o", alpha=alpha, linestyle="", label=name)

    plt.legend()
    plt.savefig('prove.png')


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

    with open("iris_100_42_norm.json", 'w') as output:
        json.dump(data, output, indent=1)
