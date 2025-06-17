# import os
import platform
import subprocess
import os
def open_directory(path: str):
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a valid directory.")
        return

    system_name = platform.system()

    try:
        if system_name == "Windows":
            os.startfile(path)
        elif system_name == "Darwin":  # macOS
            subprocess.run(["open", path])
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", path])
        print(f"Opened directory: {path}")
    except Exception as e:
        print(f"Failed to open directory: {e}")

# Example usage
if __name__ == "__main__":
    directory_path = "/Volumes/Sembark/laravel/laravel_test"
    open_directory(directory_path)


from pathlib import Path
import platform
import subprocess

def open_directory(path_str: str):
    path = Path(path_str).expanduser().resolve()

    if not path.is_dir():
        print(f"Error: '{path}' is not a valid directory.")
        return

    system_name = platform.system()

    try:
        if system_name == "Windows":
            # Works only on Windows
            os.startfile(path)
        elif system_name == "Darwin":  # macOS
            subprocess.run(["open", str(path)])
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", str(path)])
        print(f"Opened directory: {path}")
    except Exception as e:
        print(f"Failed to open directory: {e}")

# Example usage
if __name__ == "__main__":
    directory_path = input("Enter the path to the directory: ").strip()
    open_directory(directory_path)
