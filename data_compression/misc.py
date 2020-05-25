import matplotlib.pyplot as plt
import json


def scatterPlot(df, alpha):
    groups = df.groupby("species")
    n_p = len(df)
    for name, group in groups:
        plt.plot(group["f1"], group["f2"], marker="o", alpha=alpha, linestyle="", label=name)

    filename = "test_finale_lvq1/bandiera_{}_100".format(n_p)
    plt.legend()
    # plt.savefig(filename)