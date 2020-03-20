import os
import glob
import ntpath
import cv2
import numpy as np

from src.text_process.text_sorter import sort_y_coordinate, bind_closest_element
from settings import TEMPLATE_DIR


def extract_digits(frame_path, x_base_line=0, y_base_line=0):

    digits = []

    frame = cv2.imread(frame_path)
    digit_frame = frame[y_base_line:, x_base_line:]
    digit_gray = cv2.cvtColor(digit_frame, cv2.COLOR_BGR2GRAY)

    digit_coordinates = []
    digit_letters = []
    rect_frame = digit_frame.copy()
    # tmp_width = 0
    # tmp_height = 0
    # tmp_cnt = 0
    tmp_width = []
    tmp_height = []
    for template_path in glob.glob(os.path.join(TEMPLATE_DIR, "*.jpg")):

        template = cv2.imread(template_path, 0)
        template_file_name = ntpath.basename(template_path).replace(".jpg", "")
        if "digit_" in template_file_name:
            template_letter = template_file_name.replace("digit_", "")[0]
        else:
            if "comma" in template_file_name:
                template_letter = ","
            elif template_file_name == "min":
                template_letter = "-"
            else:
                template_letter = "+"

        template_w, template_h = template.shape[::-1]

        res = cv2.matchTemplate(digit_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            x = pt[0] + int(0.5 * template_w)
            y = pt[1] + int(0.5 * template_h)
            digit_coordinates.append([x, y])
            digit_letters.append(template_letter)
            # tmp_width += template_w
            # tmp_height += template_h
            tmp_width.append(template_w)
            tmp_height.append(template_h)
            # tmp_cnt += 1

            cv2.rectangle(rect_frame, (pt[0], pt[1]), (pt[0] + template_w, pt[1] + template_h), (0, 0, 255), 2)
            cv2.putText(rect_frame, template_letter, (x, y - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imwrite("rect_tmp.jpg", rect_frame)
    line_height = int(max(tmp_height, key=tmp_height.count))
    digit_width = int(max(tmp_width, key=tmp_width.count) * 0.8)
    # line_height = int(tmp_height / tmp_cnt * 1.5)
    # digit_width = int(tmp_width / tmp_cnt)

    y_sorted_digits, y_sorted_digit_coordinates = sort_y_coordinate(text_coordinates=digit_coordinates,
                                                                    text=digit_letters, line_thresh=line_height)

    for digit_list, digit_coordinate_list in zip(y_sorted_digits, y_sorted_digit_coordinates):

        x_sorted = sorted(zip(digit_list, digit_coordinate_list), key=lambda j: j[1][0])
        x_grouped_digits, x_grouped_digit_coordinates = bind_closest_element(bind_tuple=x_sorted,
                                                                             thresh_value=digit_width, axis=0)
        for digit_group, digit_group_coordinate in zip(x_grouped_digits, x_grouped_digit_coordinates):
            max_digit = max(digit_group, key=digit_group.count)
            max_digit_index = [i for i, d in enumerate(digit_group) if d == max_digit]
            x_digit = 0
            y_digit = 0
            for idx in max_digit_index:
                x_digit += digit_group_coordinate[idx][0]
                y_digit += digit_group_coordinate[idx][1]
            digits.append([int(x_digit / len(max_digit_index)), int(y_digit / len(max_digit_index)), max_digit])

            # tmp_dict = defaultdict(int)
            # for i in digit_group:
            #     tmp_dict[i] += 1
            # max_digit = max(tmp_dict.iteritems(), key=lambda j: j[1])

    for digit in digits:
        cv2.circle(digit_frame, (digit[0], digit[1]), 3, (0, 0, 255), -1)
        cv2.putText(digit_frame, digit[2], (digit[0], digit[1] - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imwrite("tmp.jpg", digit_frame)

    return digits, line_height, digit_width


if __name__ == '__main__':

    # extract_digits(frame_path="/media/mensa/Data/Task/ScannedOCR/input/00008-ksh1986_r_c.jpg", x_base_line=0,
    #                y_base_line=0)

    origin_frame = cv2.imread("/media/mensa/Data/Task/ScannedOCR/00065-ksh1988l_c.jpg", 0)
    _, thresh_origin = cv2.threshold(origin_frame, 170, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("origin_thresh.jpg", thresh_origin)

    extract_digits(frame_path="origin_thresh.jpg")
