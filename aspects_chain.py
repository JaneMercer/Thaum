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


def find_chain(for_aspects, chain_size, class_aspect):
    global all_aspects
    all_aspects = class_aspect

    print(" {} <---> {} : \n".format(for_aspects[0], for_aspects[1]))

    try:
        res = find_chain_for([item for item in class_aspect if item.get_name() == for_aspects[0]][0],
                             [item.get_index() for item in class_aspect if item.get_name() == for_aspects[0]][0],
                             chain_size, [])
        for items in res:
            names = [class_aspect[t].get_name() for t in items]
            print(names, "\n")

    except Exception:
        print("Invalid name/s \n")
