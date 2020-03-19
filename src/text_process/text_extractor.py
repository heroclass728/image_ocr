import json
import numpy as np

from src.digit_process.image_processing import extract_table_line
from src.digit_process.digit_templator import extract_digits
from settings import LINE_SPACING, LINE_MARGIN, LETTER_INTERVAL, WORD_INTERVAL


def extract_text_from_json(json_content_, part_idx, path_):
    word_coordinates = []
    words = []
    text = ""
    table_line = 0

    if part_idx == 0:
        crop_left = json_content_["textAnnotations"][0]["boundingPoly"]["vertices"][0]["x"]
        crop_right = json_content_["textAnnotations"][0]["boundingPoly"]["vertices"][1]["x"]
        crop_top = json_content_["textAnnotations"][0]["boundingPoly"]["vertices"][0]["y"]
        crop_bottom = json_content_["textAnnotations"][0]["boundingPoly"]["vertices"][3]["y"]
        table_line = extract_table_line(frame_path=path_, left=crop_left, right=crop_right, top=crop_top,
                                        bottom=crop_bottom)
        for _json in json_content_["textAnnotations"][1:]:
            if _json["boundingPoly"]["vertices"][2]["y"] < table_line:
                words.append(_json["description"])
                word_coordinates.append(get_word_coordinate(word_dict=_json))

    letter_column, split_line = split_letter_digit(base_line=table_line, content=json_content_)
    origin_x = letter_column[0]["boundingPoly"]["vertices"][0]["x"]
    grad = abs(letter_column[0]["boundingPoly"]["vertices"][0]["y"] -
               letter_column[0]["boundingPoly"]["vertices"][1]["y"]) / \
           abs(letter_column[0]["boundingPoly"]["vertices"][0]["x"] -
               letter_column[0]["boundingPoly"]["vertices"][1]["x"])

    for _json in letter_column:
        word_coordinates.append(get_word_coordinate(word_dict=_json, coordinate_grad=grad, origin_x=origin_x))
        words.append(_json["description"])

    digits = extract_digits(frame_path=path_, x_base_line=split_line, y_base_line=table_line)

    for digit in digits:
        x = split_line + digit[0]
        y = table_line + digit[1]
        y -= int((x - origin_x) * grad)
        word_coordinates.append([x, y])
        words.append(digit[2])

    y_sorted = sorted(zip(words, word_coordinates), key=lambda k: k[1][1])
    y_sorted_words = []
    y_sorted_word_coordinates = []
    init_y_value = y_sorted[0][1][1]
    tmp_line_word, tmp_line_coordinates = [], []

    for sorted_word, sorted_coordinate in y_sorted:
        if abs(init_y_value - sorted_coordinate[1]) < LINE_MARGIN:
            tmp_line_word.append(sorted_word)
            tmp_line_coordinates.append(sorted_coordinate)

        else:
            y_sorted_words.append(tmp_line_word[:])
            y_sorted_word_coordinates.append(tmp_line_coordinates[:])
            tmp_line_coordinates.clear()
            tmp_line_coordinates.append(sorted_coordinate)
            tmp_line_word.clear()
            tmp_line_word.append(sorted_word)
            init_y_value = sorted_coordinate[1]

    y_sorted_words.append(tmp_line_word[:])
    y_sorted_word_coordinates.append(tmp_line_coordinates[:])

    for word_list, word_coordinate_list in zip(y_sorted_words, y_sorted_word_coordinates):

        x_sorted = sorted(zip(word_list, word_coordinate_list), key=lambda j: j[1][0])

        for i, x_sorted_tuple in enumerate(x_sorted):
            x_word, x_word_coordinate = x_sorted_tuple
            if x_word_coordinate[1] < table_line:
                if x_word.isalpha() or x_word.isdigit():
                    text += x_word + " "
                else:
                    text = text[:text.rfind(" ")] + x_word + " "

            else:
                if i == 0:
                    text += x_word
                else:
                    if i == len(x_sorted) - 1:
                        text += ";"
                    if abs(x_word_coordinate[0] - x_sorted[i - 1][1][0]) < LETTER_INTERVAL:
                        continue
                    else:
                        if abs(x_word_coordinate[0] - x_sorted[i - 1][1][0]) > WORD_INTERVAL:
                            text += ";" + " " + x_word
                        else:
                            text += x_word

        text += "\n"

    return text


def get_word_coordinate(word_dict, coordinate_grad=0, origin_x=0):
    x = int(0.5 * (word_dict["boundingPoly"]["vertices"][0]["x"] + word_dict["boundingPoly"]["vertices"][1]["x"]))
    y = int(0.5 * (word_dict["boundingPoly"]["vertices"][0]["y"] + word_dict["boundingPoly"]["vertices"][3]["y"]))
    y -= int((x - origin_x) * coordinate_grad)

    return [x, y]


def split_letter_digit(base_line, content):
    mid_line = 0
    letters = []

    left_line = content["textAnnotations"][0]["boundingPoly"]["vertices"][0]["x"] - 20
    right_line = content["textAnnotations"][0]["boundingPoly"]["vertices"][1]["x"]

    lines = np.arange(left_line, right_line, LINE_SPACING)

    ret_val = False
    for line in lines[1:]:
        for _json in content["textAnnotations"][1:]:
            if _json["boundingPoly"]["vertices"][0]["y"] < base_line:
                continue
            if _json["boundingPoly"]["vertices"][0]["x"] <= line <= _json["boundingPoly"]["vertices"][1]["x"]:
                ret_val = False
                break
            ret_val = True

        if ret_val:
            mid_line = line
            break

    for _json in content["textAnnotations"][1:]:
        if _json["boundingPoly"]["vertices"][0]["y"] > base_line and \
                _json["boundingPoly"]["vertices"][1]["x"] < mid_line:
            letters.append(_json)

    return letters, mid_line


if __name__ == '__main__':
    path = "/media/mensa/Data/Task/ScannedOCR/output/temp_0.jpg"
    with open('/media/mensa/Data/Task/ScannedOCR/temp/temp_00001-ksh1987_l_temp_0.json') as f:
        json_content = json.load(f)

    name_ = extract_text_from_json(json_content_=json_content, path_=path, part_idx=0)
    print(name_)
