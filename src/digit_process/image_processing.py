import os
import json
import math
import cv2
import numpy as np

from settings import SAMPLE_SIZE, OUTPUT_DIR


def separate_frame_by_size(f_path):
    origin_frame = cv2.imread(f_path, 0)
    thresh_frame = cv2.threshold(origin_frame, 170, 255, cv2.THRESH_BINARY_INV)[1]
    temp_path = os.path.join(OUTPUT_DIR, "temp.jpg")
    cv2.imwrite(temp_path, thresh_frame)
    f_size = os.path.getsize(temp_path) / (1024 * 1024)
    part_cnt = int(f_size // SAMPLE_SIZE + 1)
    frame = cv2.imread(temp_path)
    frame_height = frame.shape[0]
    part_tmp_path = []
    for i in range(part_cnt):
        if i == 0:
            part_frame = frame[int(i / part_cnt * frame_height):int((i + 1) / part_cnt * frame_height), :]
        else:
            part_frame = frame[int(i / part_cnt * frame_height) - 30:int((i + 1) / part_cnt * frame_height), :]

        part_path = os.path.join(OUTPUT_DIR, "temp_{}.jpg".format(i))
        cv2.imwrite(part_path, part_frame)
        part_tmp_path.append(part_path)

    return part_tmp_path


def extract_table_line(frame_path, left, right, top, bottom):
    frame = cv2.imread(frame_path)
    crop_frame = frame[top:bottom, left:right]
    gray_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
    # _, thresh_frame = cv2.threshold(gray_frame, 170, 255, cv2.THRESH_BINARY_INV)
    dilate_frame = cv2.dilate(gray_frame, np.ones((5, 5), np.uint8), iterations=2)
    min_line_length = frame.shape[1] * 0.4
    max_line_gap = 50
    lines = cv2.HoughLinesP(dilate_frame, 1, np.pi / 180, 100, minLineLength=min_line_length, maxLineGap=max_line_gap)
    line_y = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x1 - x2) < 150:
            continue
        line_y.append(y2)
        cv2.line(crop_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    #
    cv2.imwrite('../../utils/tmp.jpg', crop_frame)
    last_line = max(line_y) + top

    return last_line


def do_image_correction(frame_path, txt_json):
    frame = cv2.imread(frame_path, 0)
    height, width = frame.shape[:2]
    base_vec = [width, 0]
    last_word = txt_json['fullTextAnnotation']['pages'][0]['blocks'][0]['paragraphs'][0]['words'][0]
    line_start_point = last_word["symbols"][0]["boundingBox"]["vertices"][3]
    line_end_point = last_word['symbols'][-1]["boundingBox"]["vertices"][3]
    word_vec = [line_end_point['x'] - line_start_point['x'],
                line_end_point['y'] - line_start_point['y']]

    angle = math.acos(((word_vec[0] * base_vec[0]) + (word_vec[1] * base_vec[1]))
                      / ((math.sqrt(word_vec[0] ** 2 + word_vec[1] ** 2)) *
                         (math.sqrt(base_vec[0] ** 2 + base_vec[1] ** 2))))
    if word_vec[1] <= 0:
        angle = angle * 180 / np.pi
    else:
        angle = - (angle * 180 / np.pi)

    # thresh_frame = cv2.threshold(frame, 180, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imwrite("thresh.jpg", thresh_frame)
    # coords = np.column_stack(np.where(thresh_frame > 0))
    # angle = cv2.minAreaRect(coords)[-1]
    #
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    print(angle)
    # angle = 0.0678568
    center_pt = (width // 2, height // 2)
    rotation_mat = cv2.getRotationMatrix2D(center_pt, angle, 1.0)
    rotated_frame = cv2.warpAffine(frame, rotation_mat, (width, height), flags=cv2.INTER_CUBIC,
                                   borderMode=cv2.BORDER_REPLICATE)
    #
    # rotated_frame = imutils.rotate_bound(frame, angle)
    cv2.imshow("rotated image", cv2.resize(rotated_frame, (800, 600)))
    cv2.imshow("origin image", cv2.resize(frame, (800, 600)))
    cv2.waitKey()


if __name__ == '__main__':
    # separate_frame_by_size(f_path="")
    # extract_table_line(frame_path="/input/00065-ksh1988l.jpg", left=400, right=4000,
    #                    top=30, bottom=3000)
    with open('/media/mensa/Data/Task/ScannedOCR/temp/temp_00001-ksh1987_l_temp_2.json') as f:
        json_content = json.load(f)
    do_image_correction(frame_path="/media/mensa/Data/Task/ScannedOCR/output/temp_2.jpg", txt_json=json_content)
