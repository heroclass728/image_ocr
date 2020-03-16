# ScannedOCR

## Overview

This project is to extract the whole information from the scanned document. It uses Google Vision API as an OCR module.

## Structure

- input

    The directory to contain the images to do ocr.

- output

    The directory to save the OCR result as a text

- src

    The source code to do OCR and extract the necessary information
    
- utils

    * The source code for image processing
    * The source code to communicate with Google Vision API
    * The source code to manage the folder and files in this project
    * The Google Vision key in the credential directory

- app

    The main execution file
    
- requirements

    All the dependencies for this project
    
- settings

    The path of directory and file

## Installation

- Environment

    Ubuntu 18.04, Python 3.6+

- Dependency Installation

    ```
        pip3 install -r requirements.txt
    ```

## Execution

- Please copy all the images into the input directory and you credential key to utils/credential directory.

- Please go ahead the directory in this project and run the following command in terminal

    ```
        python3 app.py
    ```

- The result text files are saved in output directory
