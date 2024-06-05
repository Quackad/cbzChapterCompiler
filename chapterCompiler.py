import os
import zipfile
import argparse 
import tkinter as tk
from tkinter import filedialog

def labelMove(parentFolder, outputFolder):
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        counter = 1

        if os.path.exists(parentFolder): 
            for root, dirs, files in os.walk(parentFolder):
                    for file in files:
                            if file.lower().endswith('.cbz', '.zip'):
                                cbz_path = os.path.join(root, file)
                            
                                try: 
                                    #CBZ Extraction
                                    with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
                                        for member in zip_ref.namelist():
                                            if member.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                                extracted_path = os.path.join(outputFolder, f"{counter:03d}.jpg")
                                                zip_ref.extract(member, outputFolder)
                                                os.rename(os.path.join(outputFolder, member), extracted_path)
                                                counter += 1
                                except zipfile.BadZipFile:
                                     print(f"Error: {cbz_path} is not a valid zip.")
                                except Exception as e:
                                    print(f"An unexpected error occurred while processing {cbz_path}:")
                    for dir in dirs:
                        subdir_path = os.path.join(root, dir)
                        for subdir_root, subdir_dirs, subdir_files in os.walk(subdir_path):
                            for subdir_file in subdir_files:
                                if subdir_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                    original_path = os.path.join(subdir_root, subdir_file)
                                    extracted_path = os.path.join(outputFolder, f"{counter:03d}.jpg")
                                    os.rename(original_path, extracted_path)
                                    counter += 1
        else:
            print("Specified directory does not exist, Contact Dario")

def browseButton(entry):
     filename = filedialog.askdirectory()
     entry.delete(0, tk.END)
     entry.insert(0, filename)

def executeExtraction(input_folder, output_folder):
     labelMove(input_folder.get(), output_folder.get())
    
def main():
    root = tk.Tk()
    root.title("CBZ Chapter Compiler")

    input_folder_label = tk.Label(root, text="Input Folder:")
    input_folder_label.grid(row=0, column=0, padx=5, pady=5)

    input_folder_entry = tk.Entry(root, width=50)
    input_folder_entry.grid(row=0, column=1, padx=5, pady=5)

    input_folder_button = tk.Button(root, text="Browse", command=lambda: browseButton(input_folder_entry))
    input_folder_button.grid(row=0, column=2, padx=5, pady=5)

    output_folder_label = tk.Label(root, text="Output Folder:")
    output_folder_label.grid(row=1, column=0, padx=5, pady=5)

    output_folder_entry = tk.Entry(root, width=50)
    output_folder_entry.grid(row=1, column=1, padx=5, pady=5)

    output_folder_button = tk.Button(root, text="Browse", command=lambda: browseButton(output_folder_entry))
    output_folder_button.grid(row=1, column=2, padx=5, pady=5)

    execute_button = tk.Button(root, text="Compile to Volume", command=lambda: executeExtraction(input_folder_entry, output_folder_entry))
    execute_button.grid(row=2, column=1, padx=5, pady=5)

    root.mainloop()
    
if __name__ == "__main__":
    main()
