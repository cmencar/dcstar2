import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import skfuzzy as fuzz

original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', header=None)
data = original_dataset.T.values[:-1, :]
ncenters = 3

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(data, ncenters, 2, error=0.005, maxiter=1000, init=None)
