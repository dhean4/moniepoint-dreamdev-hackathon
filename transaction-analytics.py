import os
from datetime import datetime
from collections import defaultdict



def main():
    base_folder = "./mp-hackathon-sample-data"
    if not os.path.exists(base_folder):
        print(f"ERROR: Base folder not found: {base_folder}")
        return

    subfolders = []
    for entry in os.listdir(base_folder):
        sub_path = os.path.join(base_folder, entry)
        if os.path.isdir(sub_path):
            subfolders.append(sub_path)

    if not subfolders:
        print(f"No subfolders found in {base_folder}")
        return

    total_txt_files = 0
    for folder in subfolders:
        txt_files_count = sum(1 for fn in os.listdir(folder) if fn.endswith(".txt"))
        total_txt_files += txt_files_count

        analyze_transaction_data(folder)

    if total_txt_files == 2024:
        print(f"\nAll 2024 transaction files were processed successfully!")
    else:
        print(f"\nWARNING: Expected 2024 .txt files, but found {total_txt_files}")

if __name__ == "__main__":
    main()