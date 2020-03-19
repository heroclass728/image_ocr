import os
import glob
import ntpath
import cv2
import numpy as np

from settings import TEMPLATE_DIR


def extract_digits(frame_path, x_base_line, y_base_line):

    digits = []

    frame = cv2.imread(frame_path)
    digit_frame = frame[y_base_line:, x_base_line:]
    digit_gray = cv2.cvtColor(digit_frame, cv2.COLOR_BGR2GRAY)

    digit_coordinates = []

    for template_path in glob.glob(os.path.join(TEMPLATE_DIR, "*.jpg")):

        template = cv2.imread(template_path, 0)
        template_file_name = ntpath.basename(template_path).replace(".jpg", "")
        if "digit_" in template_file_name:
            template_letter = template_file_name.replace("digit_", "")[0]
        else:
            if template_file_name == "comma":
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
            if [x, y] in digit_coordinates:
                continue
            digit_coordinates.append([x, y])
            digits.append([x, y, template_letter])
            cv2.rectangle(digit_frame, pt, (pt[0] + template_w, pt[1] + template_h), (0, 0, 255), 2)
            cv2.putText(digit_frame, template_letter, (pt[0] - 150, pt[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imwrite("tmp.jpg", digit_frame)

    return digits


if __name__ == '__main__':

    extract_digits(frame_path="/media/mensa/Data/Task/ScannedOCR/input/00008-ksh1986_r_c.jpg", x_base_line=0,
                   y_base_line=0)
