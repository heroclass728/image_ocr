import os
import cv2
import numpy as np

from settings import SAMPLE_SIZE, OUTPUT_DIR


def separate_frame_by_size(f_path):

    frame = cv2.imread(f_path)
    _, thresh_frame = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 180, 255, cv2.THRESH_BINARY_INV)
    dilate_frame = cv2.dilate(thresh_frame, np.ones((2, 2), np.uint8), iterations=1)
    thresh_frame_path = os.path.join(OUTPUT_DIR, "temp.jpg")
    cv2.imwrite(thresh_frame_path, dilate_frame)

    f_size = os.path.getsize(thresh_frame_path) / (1024 * 1024)
    part_cnt = int(f_size // SAMPLE_SIZE + 1)
    frame = cv2.imread(f_path)
    frame_height = frame.shape[0]
    part_tmp_path = []
    for i in range(part_cnt):
        if i == 0:
            part_frame = dilate_frame[int(i / part_cnt * frame_height):int((i + 1) / part_cnt * frame_height), :]
        else:
            part_frame = dilate_frame[int(i / part_cnt * frame_height) - 30:int((i + 1) / part_cnt * frame_height), :]

        part_path = os.path.join(OUTPUT_DIR, "temp_{}.jpg".format(i))
        cv2.imwrite(part_path, part_frame)
        part_tmp_path.append(part_path)

    return part_tmp_path


def extract_table_line(frame_path, left, right, top, bottom):

    frame = cv2.imread(frame_path)
    crop_frame = frame[top-30:bottom+30, left-30:right+30]
    thresh_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
    # dilate_frame = cv2.dilate(crop_frame, np.ones((5, 5), np.uint8), iterations=2)
    # cv2.imwrite("tmp.jpg", dilate_frame)
    min_line_length = frame.shape[1] * 0.6
    max_line_gap = 50
    lines = cv2.HoughLinesP(thresh_frame, 1, np.pi / 180, 100, minLineLength=min_line_length, maxLineGap=max_line_gap)
    line_y = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        line_y.append(y2)
        # cv2.line(crop_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # cv2.imwrite('tmp.jpg', crop_frame)
    last_line = max(line_y) + top

    return last_line


if __name__ == '__main__':

    # separate_frame_by_size(f_path="")
    extract_table_line(frame_path="/media/mensa/Data/Task/ScannedOCR/output/temp_0.jpg", left=0, right=0, top=0,
                       bottom=0)
