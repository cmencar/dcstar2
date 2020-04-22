import matplotlib.pyplot as plt


def scatterPlot(df):
    groups = df.groupby("classes")
    for name, group in groups:
        plt.plot(group["feature1"], group["feature2"], marker="o", linestyle="", label=name)

    plt.legend()
    plt.savefig('test/bandiera/bandiera_30.png')
    plt.show()
