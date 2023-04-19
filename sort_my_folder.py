import shutil
import os
import sys
from os import walk
from os.path import splitext
from transliterate import translit
from string import ascii_letters, digits

CATEGORIES = {"images": ("jpeg", "png", "jpg", "svg"),
              "video": ("avi", "mp4", "mov", "mkv"),
              "documents": ("doc", "docx", "txt", "pdf", "xlsx", "pptx", "djvu "),
              "audio": ("mp3", "ogg", "wav", "amr"),
              "archives": ("zip", "gz", "tar")
              }

ALL_EXTENSIONS = ("jpeg", "png", "jpg", "svg", "avi", "mp4", "mov", "mkv", "doc", "docx", "txt", "pdf", "xlsx", "pptx",
                  "mp3", "ogg", "wav", "amr", "zip", "gz", "tar")

IGNORED_FOLDERS = ("archives", "video", "audio", "documents", "images", "other_formats")

known_extensions = set()
unknown_extensions = set()


def get_path_dir():
    try:
        abs_path = sys.argv[1]
        if os.path.isdir(abs_path):
            return abs_path
        else:
            raise IsADirectoryError
    except Exception:
        print("Something went wrong. Please try again.")
        exit()


# rename and normalize all files in given directory
def normalize(name):
    transliterated = translit(name, language_code="ru", reversed=True)
    normalized_name = "".join([char if char in ascii_letters or char in digits else "_" for char in transliterated])
    return normalized_name


def delete_empty_folders(path):
    # searching empty folders
    folders = os.listdir(path)
    if len(folders):
        for folder in folders:
            if folder not in IGNORED_FOLDERS:
                full_path = os.path.join(path, folder)
                if os.path.isdir(full_path):
                    delete_empty_folders(full_path)
    # remove empty folder
    if len(folders) == 0:
        os.rmdir(path)


def change_directory(path_to_folder, full_path_file, new_file_name):
    if not os.access(path_to_folder, os.F_OK):
        os.mkdir(path_to_folder)

    # if the file exists in the target directory → delete the file to be moved
    if not os.access(f"{path_to_folder}\\{new_file_name}", os.F_OK):
        shutil.move(full_path_file, f"{path_to_folder}\\")
    else:
        os.remove(full_path_file)


def unpack_archive(path_to_folder, new_file_name):
    archive_folder = path_to_folder + splitext(new_file_name)[0]
    os.mkdir(archive_folder)
    shutil.unpack_archive(path_to_folder + new_file_name, archive_folder)  # shutil doesn't work with .tar format; use the tarfile module

    # after renaming → delete old archive
    os.remove(path_to_folder + new_file_name)


def sort_files(path):
    for root, folders, files in walk(path, topdown=True):

        current_directory = root.split("\\")[-1]
        if current_directory in IGNORED_FOLDERS:
            continue

        # rename files and move them
        for file in files:
            old_name, ext_file = splitext(file)  # file name and file extension of each files
            new_file_name = normalize(old_name) + ext_file

            full_path_file = f"{root}\\{new_file_name}"
            os.rename(f"{root}\\{file}", full_path_file)

            if ext_file[1:] in ALL_EXTENSIONS:
                for category, formats in CATEGORIES.items():
                    if ext_file[1:] in formats:
                        change_directory(f"{path}\\{category}", full_path_file, new_file_name)
                        if category == "archives":
                            unpack_archive(f"{path}\\{category}\\", new_file_name)

            else:
                # move file to the folder "other_formats" if its extension not in ALL_EXTENSIONS set
                change_directory(f"{path}\\other_formats", full_path_file, new_file_name)


def get_files_info(path):
    with open("files_information.txt", "w") as txt_file:
        folders_list = os.listdir(path)

        for folder in folders_list:
            txt_file.write(f"***{folder}***\n")

            files_list = os.listdir(f"{path}\\{folder}")
            for file in files_list:
                txt_file.write(f"{file}\n")
                if folder != "other_formats":
                    known_extensions.add(splitext(file)[1])
                else:
                    unknown_extensions.add(splitext(file)[1])
            txt_file.write("\n\n")

        txt_file.write(f"known_extensions\t{known_extensions}\n")
        txt_file.write(f"unknown_extensions\t{unknown_extensions}\n")


def main():
    path_to_dir = get_path_dir()
    sort_files(path_to_dir)

    delete_empty_folders(path_to_dir)
    get_files_info(path_to_dir)  # write information to txt file


if __name__ == "__main__":
    main()
