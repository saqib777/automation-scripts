"""Bulk Rename Files Script"""
import os

def rename_files_in_directory(directory, prefix):
    """Renames all files in a directory with a given prefix."""
    for i, filename in enumerate(os.listdir(directory)):
        old_path = os.path.join(directory, filename)
        if os.path.isfile(old_path):
            new_name = f"{prefix}_{i}{os.path.splitext(filename)[1]}"
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")

if __name__ == "__main__":
    rename_files_in_directory(".", "file")
