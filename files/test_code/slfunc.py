# FUNCTION THAT SELECTS THE TOP N ITEMS FROM A RECOMMENDATION LIST FOR EACH USER


def select_top_items(number_of_top_items, full_recomendation_list):
    n = number_of_top_items
    frl = full_recomendation_list
    top_list = {}

    for i in frl:
        top_list[i] = {k: frl[i][k] for k in sorted(frl[i], key=lambda k: -frl[i][k])[:n]}

    return top_list
