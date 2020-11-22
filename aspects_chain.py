import numpy as np

all_aspects = []


def find_chain_for(for_aspect, to_aspect, length, arr_to_append):
    indx = for_aspect.get_index()
    dependencies = for_aspect.get_dependencies()

    if length <= 1:
        for item in dependencies:
            if item == to_aspect:
                arr_to_append.append([indx, item])
        if arr_to_append:
            return arr_to_append
        else:
            # print("None \n")
            return []
    elif length < 1:
        print("Length is less then 1")
    else:
        i = 0
        for x in dependencies:
            res_arr = []

            find_chain_for(all_aspects[x], to_aspect, length - 1, res_arr)

            for el in res_arr:
                el.insert(0, indx)
                arr_to_append.append(el)
            # arr_to_append.append(([item[1] for item in res_arr if item[0] == x]))
            # print(res_arr)
            i += 1
        return arr_to_append


def count_value(chains, max_result):
    chain_sum_tuple = []
    res = []
    for chain in chains:
        value = sum([all_aspects[t].get_value() for t in chain])
        print(value)

        arr_size = chain_sum_tuple.__len__()
        if arr_size == 0:
            chain_sum_tuple.insert(0,(chain, value))
        elif 0 < arr_size :
            ch, val = chain_sum_tuple[arr_size-1]
            if val > value:
                chain_sum_tuple.insert(arr_size-1, (chain, value))
            elif val == value:
                pass
            else:
                chain_sum_tuple.insert(arr_size, (chain, value))

            if arr_size >= max_result:
                del chain_sum_tuple[-1]

    if chain_sum_tuple.__len__() > 0:
        for elem in chain_sum_tuple:
            ch, val = elem
            res.append(ch)

    return res






def find_chain(for_aspects, chain_size, class_aspect):
    global all_aspects
    all_aspects = class_aspect

    numpy_vert_concat = []

    print(" {} <---> {} : \n".format(for_aspects[0], for_aspects[1]))

    try:
        res = find_chain_for([item for item in class_aspect if item.get_name() == for_aspects[0]][0],
                             [item.get_index() for item in class_aspect if item.get_name() == for_aspects[1]][0],
                             chain_size, [])

        if res:

            best_strings = count_value(res, 3)
            for items in best_strings:
                names = [class_aspect[t].get_name() for t in items]
                print(names, "\n")
                numpy_horizontal_concat = np.concatenate([class_aspect[t].get_image() for t in items], axis=1)
                numpy_vert_concat.append(numpy_horizontal_concat)
            return np.concatenate([t for t in numpy_vert_concat], axis=0)
        else:
            print("No chain found")
            return []

    except Exception:
        print("Invalid name/s \n")
        return []
