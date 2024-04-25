import lzma
import os
import glob


def extract_xz_files(root_dir):
    # Walk through the directory
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json.xz"):
                # Construct full file path
                full_file_path = os.path.join(root, file)
                print(f"Extracting: {full_file_path}")

                # Open the .xz file
                with lzma.open(full_file_path) as compressed:
                    content = compressed.read()

                    # Construct the new filename (.json)
                    new_file_path = full_file_path[:-3]  # Remove .xz

                    # Write the decompressed content to a new .json file
                    with open(new_file_path, "wb") as decompressed:
                        decompressed.write(content)
                print(f"Extracted to: {new_file_path}")


# Example usage:
root_directory = "/Users/arham/Downloads/Social Media/Individual Assignment/Data"  # Change this to your root directory
extract_xz_files(root_directory)
