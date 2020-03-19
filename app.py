import glob
import os
import ntpath

from settings import INPUT_DIR, OUTPUT_DIR
from src.text_process.ocr_text import process_ocr_text
from utils.folder_file_manager import log_print, extract_file_name, save_file


if __name__ == '__main__':

    input_image_path = glob.glob(os.path.join(INPUT_DIR, "*.*"))
    processed_files = glob.glob(os.path.join(OUTPUT_DIR, "*.*"))
    processed_file_names = []

    for processed_f_path in processed_files:
        f_name = extract_file_name(file_path=processed_f_path)
        processed_file_names.append(f_name)

    total_lens = len(input_image_path)
    for i, path in enumerate(input_image_path):

        file_name = ntpath.basename(path).replace(".jpg", "")
        if file_name in processed_file_names:
            continue

        print("Process {}-({} / {})".format(path, i + 1, total_lens))
        try:
            frame_content = process_ocr_text(frame_path=path)
            txt_file_path = os.path.join(OUTPUT_DIR, "{}.txt".format(file_name))
            save_file(content=frame_content, filename=txt_file_path, method='w')
            log_print(info_str=path + "\n" + "Successfully processed")
            print("Successfully processed {}".format(path))

        except Exception as e:
            log_print(info_str=path)
            log_print(info_str=e)

    for jpg_path in glob.glob(os.path.join(OUTPUT_DIR, "*.jpg")):
        os.remove(jpg_path)
