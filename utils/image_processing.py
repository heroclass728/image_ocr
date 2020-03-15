import os
import cv2

from settings import SAMPLE_SIZE, OUTPUT_DIR


def separate_frame_by_size(f_path):

    f_size = os.path.getsize(f_path) / (1024 * 1024)
    part_cnt = int(f_size // SAMPLE_SIZE + 1)
    frame = cv2.imread(f_path)
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


if __name__ == '__main__':

    separate_frame_by_size(f_path="")
