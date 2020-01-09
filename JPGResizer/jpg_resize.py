from PIL import Image
from datetime import datetime as dt

import os


SAVE_DIR = r"C:\Users\dell\Desktop"
now = dt.utcnow().strftime('%y%m%d-%H%M%S')

def main():
    file = str(input("Enter the file path: "))

    file_is_present = os.path.isfile(file)
    assert file_is_present, "Inputted File path doesn't exist"

    width = int(input("Enter the width: "))
    height = int(input("Enter the height: "))

    f_path = os.path.join(SAVE_DIR, f"image_{width}_{height}_{now}.jpg")

    img = Image.open(file)
    img = img.resize((width, height))

    try:
        img.save(f_path)
    except OSError:
        print("Script doesn't work for PNG files")
        exit()
    else:
        print(f"Successfully saved in {SAVE_DIR}")

main() if __name__ == "__main__" else None
    