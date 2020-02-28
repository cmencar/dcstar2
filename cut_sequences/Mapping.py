import T_d_bin as bc
import S_d as sc
import HyperboxesSet as hb
import numpy as np
import itertools as itool


# Function for converting a logical cut sequence to
# a point-based cut sequence
# @T_d: general cut sequence
# @S_d_bin: logical cut sequence
def from_logical_to_point(T_d, S_d_bin):

    # definition of a new S_d sequence of selected cuts
    S_d = sc.SelectedCuts()

    # if logical cut sequence is empty then return an empty S_d
    if S_d_bin.get_dimensions_number() < 1:
        return S_d
    else:

        # for each dimension of S_d_bin logical sequence cut
        for dimension_index in range(1, S_d_bin.get_dimensions_number() + 1):

            # if dimension referred by dimension_index is empty then
            # set an empty NumPy array
            if S_d_bin.get_dimension_size(dimension_index) < 1:
                S_d.set_dimension(dimension_index, np.array([]))
            else:

                # definition of a temporary element's list for the evaluated dimension
                dimension_elements = list()

                # definition of an index for the temporary element's list
                dimension_element_index = 0

                # for each element in dimension referred by dimension_index
                for element_index in range(1, S_d_bin.get_dimension_size(dimension_index) + 1):

                    # if cut logical value set in dimension referred by dimension_index at
                    # position referred by element_index is True, then insert into the
                    # temporary element's list the corrisponding point-based value of
                    # T_d cut sequence
                    if S_d_bin.get_cut(dimension_index, element_index):
                        dimension_elements.insert(dimension_element_index, T_d.get_dimension(dimension_index)[element_index - 1])
                        dimension_element_index = dimension_element_index + 1

                # insert a new dimension in S_d structure
                S_d.set_dimension(dimension_index, dimension_elements)

        # return complete S_d structure
        return S_d


# Function for converting a point-based cut sequence to
# a logical cut sequence to
# @T_d: general cut sequence
# @S_d: point-based cut sequence
def from_point_to_logical(T_d, S_d):

    # definition of a new S_d sequence of selected cuts
    S_d_bin = bc.BinaryCuts()

    # if cut sequence is empty then return an S_d_bin
    # with every logical value set to False
    if S_d.get_dimensions_number() < 1:
        return generate_starting_binary_t_d(T_d)
    else:

        # for each dimension of T_d cut sequence
        for dimension_index in range(1, T_d.get_dimensions_number() + 1):

            # definition of a temporary element's list for the evaluated dimension
            dimension_elements = list()

            # definition of indexes for scanning the NumPy arrays
            T_d_index = 0
            S_d_index = 0

            # until the scan of all elements in the T_d array is completed
            while T_d_index < T_d.get_dimension_size(dimension_index):

                # if S_d's dimension referred is an empty NumPy array then
                # insert a False logical value for each T_d corrisponding element
                # and increment T_d_index
                if S_d.get_dimension_size(dimension_index) == 0 or S_d.get_dimension_size(dimension_index) <= S_d_index:
                    dimension_elements.append(False)
                    T_d_index = T_d_index + 1

                # if T_d's dimension value referred is lower than S_d's dimension
                # value referred then insert a False logical value for that
                # element and increment T_d_index
                elif T_d.get_dimension(dimension_index)[T_d_index] < S_d.get_dimension(dimension_index)[S_d_index]:
                    dimension_elements.append(False)
                    T_d_index = T_d_index + 1

                # if T_d's dimension value referred is equal to S_d's dimension
                # value referred then insert a True logical value for that
                # element and increment both T_d_index and S_d_index
                elif T_d.get_dimension(dimension_index)[T_d_index] == S_d.get_dimension(dimension_index)[S_d_index]:
                    dimension_elements.append(True)
                    T_d_index = T_d_index + 1
                    S_d_index = S_d_index + 1

            # inserting the list of logical elements, made by T_d element's presence
            # into S_d structure, into S_d_bin structure (converting automatically
            # the list into a NumPy array)
            S_d_bin.set_dimension(dimension_index, dimension_elements)

    # return complete S_d_bin structure
    return S_d_bin


# Function for converting a general cut sequence to
# a logical cut sequence, where each element (corresponding
# an element of T_d) is a False logical value
# @T_d: general cut sequence
def generate_starting_binary_t_d(T_d):

    # definition of a new list of logical value
    T_d_bin = list()

    # for each dimension of T_d sequence cut
    for dimension_index in range(1, T_d.get_dimensions_number() + 1):

        # definition of a list of logical value for referred dimension
        dimension = list()

        # for each element in dimension referred by dimension_index
        # insert a False logical value
        for element in T_d.get_dimension(dimension_index):
            dimension.append(False)

        # insert the logical value cut dimension's list
        # into T_d_bin
        T_d_bin.insert(dimension_index, dimension)

    # return a BinaryCuts object using T_d_bin elements
    return bc.BinaryCuts(T_d_bin)


def S_d_to_hyperboxes(S_d):

    hyperboxes = hb.HyperboxesSet()

    # TODO inserisci m_d e M_d

    intervals = list()

    for dimension_index in range(1, S_d.get_dimensions_number() + 1):

        dimension = S_d.get_dimension(dimension_index)
        n_element = S_d.get_dimension_size(dimension_index)

        dimension_intervals = list()

        if n_element > 1:
            for x in range(0, n_element-1):
                dimension_intervals.append((dimension[x], dimension[x+1]))

        intervals.append(dimension_intervals)

    interr = list()

    for i in intervals:
        if i:
            interr.append(i)


    #cartesio = itool.product(*interr)

    for element in itool.product(*interr):
        print(element)

    #print(cartesio)

    return hyperboxes