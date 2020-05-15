import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,


fig1 = plt.figure()

# Fixing random state for reproducibility
np.random.seed(19680801)

data = np.random.rand(2, 25)
l, = plt.plot([], [], 'r-')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
                                   interval=50, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

"""
colnames = ('f1', 'f2', 'species')
data = pd.read_csv('dataset_bidimensionali/datacerchiconcentrici_3classi(pieni)(classiNum).csv', names=colnames)

X = data.iloc[:, :-1].to_numpy()
# fit the fuzzy-c-means
fcm = FCM(n_clusters=3)
fcm.fit(X)

# outputs
fcm_centers = fcm.centers
fcm_labels = fcm.u.argmax(axis=1)

# plot result
f, axes = plt.subplots(1, 2, figsize=(11, 5))
scatter(X[:, 0], X[:, 1], ax=axes[0])
scatter(X[:, 0], X[:, 1], ax=axes[1], hue=fcm_labels)
scatter(fcm_centers[:, 0], fcm_centers[:, 1], ax=axes[1], marker="s", s=200)
plt.show()
"""
