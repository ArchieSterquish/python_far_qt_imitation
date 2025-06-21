import os
import subprocess
import shutil

HOME_DIRECTORY = '/home/archie' # for debugging purposes

class SystemAPI:
    def get_files_and_directories_list(
            path="~/",
            do_sort = True,
            show_hidden = False):
        files_list = SystemAPI.get_files_list(path,do_sort,show_hidden)
        dirs_list  = SystemAPI.get_directories_list(path,do_sort,show_hidden)

        return (files_list,dirs_list)

    def get_files_list(
            path="~/",
            do_sort = True,
            show_hidden = False):
        all_items = os.listdir(path)

        if not show_hidden:            
            files = [item for item in all_items if not os.path.isdir(os.path.join(path, item)) and not item.startswith(".")]
        else:
            files = [item for item in all_items if not os.path.isdir(os.path.join(path, item))]
        
        if do_sort:
            files.sort(key=str.lower)

        return files

    def get_directories_list( 
            path="~/",
            do_sort = True,
            show_hidden = False):
        all_items = os.listdir(path)
        if not show_hidden:            
            directories = [item for item in all_items if os.path.isdir(os.path.join(path, item)) and not item.startswith(".")]
        else:
            directories = [item for item in all_items if os.path.isdir(os.path.join(path, item))]

        # to get files in order
        if do_sort:
            directories.sort(key=str.lower)

        if (path != "/"):  # root directory so we don't add .. 
            directories = ['..'] + directories
        return directories

    def basename(path):
        return os.path.basename(path)

    def dirname(path):
        return os.path.dirname(path)

    def join(path,additional_dir):
        return os.path.join(path,additional_dir)

    def remove_file_or_directory(path):
        try:
            if not path.startswith(HOME_DIRECTORY):
                print('Error: not in home directory (sorry) but I\'m scared to work with root folders or files')
                return
            if SystemAPI.basename(path) == "..":
                print('Error: trying to delete using ..')
                return

            if os.path.exists(path):
                if SystemAPI.is_file(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
        except FileNotFoundError:
            print(f"Error: Directory '{dir_path}' not found.")

    def make_directory(path,dir_name):
        try:
            os.mkdir(os.path.join(path,dir_name))
        except OSError as error:
            return str(error)

    def is_file(path):
        return not os.path.isdir(path)

    def open_file_in_editor(path):
        os.system(f"kitty nvim {path}")

    def execute_command(command):
        os.system(f"kitty {command}")
