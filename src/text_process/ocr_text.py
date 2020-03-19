import json
import os
import ntpath

from src.text_process.text_extractor import extract_text_from_json
from utils.folder_file_manager import save_file
from utils.google_ocr import GoogleVisionAPI
from src.digit_process.image_processing import separate_frame_by_size
from settings import LOCAL, CUR_DIR

google_ocr = GoogleVisionAPI()


def process_ocr_text(frame_path):

    container = ""

    temp_paths = separate_frame_by_size(f_path=frame_path)

    for i, t_path in enumerate(temp_paths):

        image_ocr_json = google_ocr.detect_text(img_path=t_path)
        if LOCAL:
            json_file_path = os.path.join(CUR_DIR, 'temp', "temp_{}_{}.json".format(
                ntpath.basename(frame_path).replace(".jpg", ""), ntpath.basename(t_path).replace(".jpg", "")))
            save_file(filename=json_file_path, content=json.dumps(image_ocr_json), method="w")

        container += extract_text_from_json(json_content_=image_ocr_json, path_=t_path, part_idx=i) + "\n"

    return container


if __name__ == '__main__':

    process_ocr_text(frame_path="")
