import os

from utils.folder_file_manager import make_directory_if_not_exists


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'output'))
INPUT_DIR = os.path.join(CUR_DIR, 'input')

CREDENTIAL_PATH = os.path.join(CUR_DIR, 'utils', 'credential', 'Credentials-fdf02670129a.json')
SAMPLE_SIZE = 4
LINE_RATIO = 0.02

LOCAL = True
