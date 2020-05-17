import matplotlib.pyplot as plt
import json


def scatterPlot(df, alpha):
    groups = df.groupby("species")
    n_p = len(df)
    for name, group in groups:
        plt.plot(group["f1"], group["f2"], marker="o", alpha=alpha, linestyle="", label=name)

    filename = "test_finale_lvq1/bandiera_{}_100".format(n_p)
    plt.legend()
    plt.savefig(filename)


def create_json(m_d, M_d, prototypes):
    prototypes = prototypes.to_numpy()
    n_p = len(prototypes)
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

    filename = "test_finale_lvq1/bandiera_{}_100.json".format(n_p)
    with open(filename, 'w') as output:
        json.dump(data, output, indent=1)
