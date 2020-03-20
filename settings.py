import os

from utils.folder_file_manager import make_directory_if_not_exists


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'output'))
INPUT_DIR = os.path.join(CUR_DIR, 'input')
TEMPLATE_DIR = os.path.join(CUR_DIR, 'utils', 'templates')

CREDENTIAL_PATH = os.path.join(CUR_DIR, 'utils', 'credential', 'Pontiac Parole Hearings-e10c6d14f425.json')
MODEL_PATH = os.path.join(CUR_DIR, 'utils', 'model', 'digit_model.h5')

SAMPLE_SIZE = 4
LINE_MARGIN = 50
LINE_SPACING = 50
LETTER_INTERVAL = 30
WORD_INTERVAL = 100
ONE_DIGIT_WIDTH = 30

LOCAL = True
