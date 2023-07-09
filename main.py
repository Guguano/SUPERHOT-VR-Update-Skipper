import os
import re
import sys
from tkinter import Tk, filedialog
import webbrowser


def get_file_dir():
    root = Tk()
    root.withdraw()
    file_dir = filedialog.askdirectory()
    return file_dir


def get_updated_manifest_id(updated_manifest_id):
    mid_regex = re.compile("[0-9]{16,19}")

    valid_id = mid_regex.match(updated_manifest_id)
    if valid_id is not None:
        return updated_manifest_id

    url = "https://steamdb.info/depot/617831/"
    print(f"Go to {url} then copy the Manifest ID and enter it here.")
    elem = input("Would you like to open the page in your browser? [y/n] ").strip()
    valid_id = mid_regex.match(elem)
    if valid_id is not None:
        updated_manifest_id = elem
    elif elem.lower() in ["y", "ye", "yes", ""]:
        # Open URL in a new browser window
        webbrowser.open_new(url)

    if updated_manifest_id == "":
        elem = input("Enter the Manifest ID: ").strip()
        valid_id = mid_regex.match(elem)

        while valid_id is None:
            print("Error: Invalid Manifest ID. The Manifest ID should be a 16-19 digit number.")
            elem = input("Enter the Manifest ID: ").strip()
            valid_id = mid_regex.match(elem)

        updated_manifest_id = elem

    return updated_manifest_id


def update_manifest(steam_dir, updated_manifest_id):
    manifest_line_regex = re.compile("(?P<manifest_line>\"manifest\"\s*\"[0-9]+\")")
    manifest_id_regex = re.compile("\"manifest\"[\s]*\"(?P<manifest_id>[0-9]{16,19})\"")
    file_name = "appmanifest_617830.acf"
    target = os.path.join(steam_dir, "steamapps")
    target = os.path.join(target, file_name)

    # Open the manifest file in read only mode
    with open(target, 'r') as file:
        file_content = file.read()

    match_line = manifest_line_regex.match(file_content)
    if match_line is None:
        return

    line = match_line.group('manifest_line')

    match_id = manifest_id_regex.match(line)
    m_id = match_id.group('manifest_id')

    updated_manifest_id = get_updated_manifest_id(updated_manifest_id)

    updated_line = line.replace(m_id, updated_manifest_id)
    updated_file_content = file_content.replace(line, updated_line)
    # Open the manifest file in write only mode
    #with open(target, 'w') as file:
        #file.write(updated_file_content)
    print(updated_file_content)


def main():
    steam_dir = ""
    updated_manifest_id = ""
    if len(sys.argv) == 2:
        steam_dir = sys.argv[1]
    elif len(sys.argv) == 3:
        steam_dir = sys.argv[1]
        updated_manifest_id = sys.argv[2]
    else:
        print("Please select your Steam folder.")
        steam_dir = get_file_dir()

    # if the users presses "Cancel", exit as no directory was selected
    if steam_dir == "":
        return None

    update_manifest(steam_dir, updated_manifest_id)


if __name__ == '__main__':
    main()
