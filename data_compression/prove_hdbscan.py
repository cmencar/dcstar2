from sklearn.datasets import make_blobs
import pandas as pd
import hdbscan

ionosphere = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
              'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19',
              'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28',
              'f29', 'f30', 'f31', 'f32', 'f33', 'label')
original_dataset = pd.read_csv('dataset_ndimensionali/ionosphere.csv', names=ionosphere)

blobs, labels = make_blobs(n_samples=2000, n_features=10)

dataset = pd.DataFrame(blobs).head()

clusterer = hdbscan.HDBSCAN()

