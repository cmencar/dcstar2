import doubleclusteringstar as dcstar
import numpy as np


ks = [2, 3, 4, 5, 6, 7, 8, 9, 10]

# all chessboards' test are executed by DC*
for k in ks:


    print("\n---- Evaluating chessboard_k" + str(k) + ".json ----")
    filename = "RISULTATI TEST ACCURACY/bidim/chessboard/chessboard_k" + str(k) + ".json"

    # loading of prototypes point list and dimensional boundaries
    point_list, m_d, M_d = dcstar.DoubleClusteringStar.load(filename)

    clustering = dcstar.DoubleClusteringStar(prototypes=point_list, m_d=m_d, M_d=M_d, verbose=True)
    clustering.train(save_log=True)
#    clustering.plot_result()


pass