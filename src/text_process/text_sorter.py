from settings import LINE_MARGIN


def sort_y_coordinate(text, text_coordinates, line_thresh):

    y_sorted = sorted(zip(text, text_coordinates), key=lambda k: k[1][1])
    sorted_words, sorted_word_coordinates = bind_closest_element(bind_tuple=y_sorted, thresh_value=line_thresh, axis=1)

    return sorted_words, sorted_word_coordinates


def bind_closest_element(bind_tuple, thresh_value, axis):

    sorted_values = []
    sorted_value_coordinates = []
    init_value = bind_tuple[0][1][axis]
    tmp_line_value, tmp_line_coordinates = [], []

    for sorted_word, sorted_coordinate in bind_tuple:
        if abs(init_value - sorted_coordinate[axis]) < thresh_value:
            tmp_line_value.append(sorted_word)
            tmp_line_coordinates.append(sorted_coordinate)

        else:
            sorted_values.append(tmp_line_value[:])
            sorted_value_coordinates.append(tmp_line_coordinates[:])
            tmp_line_coordinates.clear()
            tmp_line_coordinates.append(sorted_coordinate)
            tmp_line_value.clear()
            tmp_line_value.append(sorted_word)
            init_value = sorted_coordinate[axis]

    sorted_values.append(tmp_line_value[:])
    sorted_value_coordinates.append(tmp_line_coordinates[:])

    return sorted_values, sorted_value_coordinates


if __name__ == '__main__':

    sort_y_coordinate(text="", text_coordinates=[])
