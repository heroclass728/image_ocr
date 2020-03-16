import json
import os
import ntpath
import cv2

from utils.folder_file_manager import save_file
from utils.google_ocr import GoogleVisionAPI
from utils.image_processing import separate_frame_by_size, extract_table_line
from settings import LOCAL, CUR_DIR, LINE_RATIO


class TextProcess:

    def __init__(self):

        self.google_ocr = GoogleVisionAPI()

    def process_ocr_text(self, frame_path):

        container = ""

        temp_paths = separate_frame_by_size(f_path=frame_path)

        for i, t_path in enumerate(temp_paths):

            image_ocr_json = self.google_ocr.detect_text(img_path=t_path)
            if LOCAL:
                json_file_path = os.path.join(CUR_DIR, 'temp', "temp_{}_{}.json".format(
                    ntpath.basename(frame_path).replace(".jpg", ""), ntpath.basename(t_path).replace(".jpg", "")))
                save_file(filename=json_file_path, content=json.dumps(image_ocr_json), method="w")

            container += self.extract_text_from_json(json_content_=image_ocr_json, path_=t_path, part_idx=i) + "\n"

        return container

    @staticmethod
    def extract_text_from_json(json_content_, part_idx, path_=None):

        word_coordinates = []
        words = []
        text = ""
        table_line = 0
        line_margin = 40

        if part_idx == 0:
            crop_left = json_content_["textAnnotations"][0]["boundingPoly"]["vertices"][0]["x"]
            crop_right = json_content_["textAnnotations"][0]["boundingPoly"]["vertices"][1]["x"]
            crop_top = json_content_["textAnnotations"][0]["boundingPoly"]["vertices"][0]["y"]
            crop_bottom = json_content_["textAnnotations"][0]["boundingPoly"]["vertices"][3]["y"]
            table_line = extract_table_line(frame_path=path_, left=crop_left, right=crop_right, top=crop_top,
                                            bottom=crop_bottom)

        for _json in json_content_["textAnnotations"][1:]:

            x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] + _json["boundingPoly"]["vertices"][1]["x"]))
            y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] + _json["boundingPoly"]["vertices"][3]["y"]))

            word_coordinates.append([x, y])
            words.append(_json["description"])

        y_sorted = sorted(zip(words, word_coordinates), key=lambda i: i[1][1])
        y_sorted_words = []
        y_sorted_word_coordinates = []
        init_y_value = y_sorted[0][1][1]
        tmp_line_word, tmp_line_coordinates = [], []

        for sorted_word, sorted_coordinate in y_sorted:
            if abs(init_y_value - sorted_coordinate[1]) < line_margin:
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

            for x_word, x_word_coordinate in x_sorted:
                if part_idx == 0 and x_word_coordinate[1] < table_line:
                    if x_word.isalpha() or x_word.isdigit():
                        text += x_word + " "
                    else:
                        text = text[:text.rfind(" ")] + x_word + " "

                else:
                    if x_word.isdigit() or x_word.isalpha():
                        text += x_word + ";" + " "
                    elif x_word == ",":
                        text = text[:text.rfind(" ") - 1] + x_word
                    else:
                        text += x_word

            text += "\n"

        return text


if __name__ == '__main__':
    text_processor = TextProcess()
    path = "/media/mensa/Data/Task/ScannedOCR/output/temp_0.jpg"
    with open('/media/mensa/Data/Task/ScannedOCR/temp/temp_00001-ksh1987_l_temp_0.json') as f:
        json_content = json.load(f)

    name_ = text_processor.extract_text_from_json(json_content_=json_content, path_=path, part_idx=0)
    print(name_)
