import os
import zipfile
import shutil
import tempfile
import tkinter as tk
from tkinter import filedialog

def labelMove(parentFolder, outputFolder, exportType):
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    counter = 1
    temp_dir = None

    if os.path.exists(parentFolder):
        try:
            temp_dir = tempfile.mkdtemp()

            for root, dirs, files in os.walk(parentFolder):
                for file in files:
                    if file.lower().endswith(('.cbz', '.zip')):
                        #(CBZ or ZIP)
                        cbz_path = os.path.join(root, file)
                        try:
                            #CBZ Extraction
                            with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
                                for member in zip_ref.namelist():
                                    if member.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                        # Extract image file to the temp directory
                                        zip_ref.extract(member, temp_dir)
                                        extracted_file = os.path.join(temp_dir, member)
                                        new_file_name = os.path.join(temp_dir, f"{counter:03d}.jpg")

                                        if os.path.exists(extracted_file):
                                            shutil.move(extracted_file, new_file_name)
                                            counter += 1
                        except zipfile.BadZipFile:
                            print(f"Error: {cbz_path} is not a valid zip.")
                        except Exception as e:
                            print(f"An unexpected error occurred while processing {cbz_path}: {e}")

                    elif file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        #Root with images
                        original_path = os.path.join(root, file)
                        new_file_name = os.path.join(temp_dir, f"{counter:03d}.jpg")
                        shutil.copy(original_path, new_file_name)
                        counter += 1

            #Export 
            if exportType.lower() == "cbz":
                cbz_filename = os.path.join(outputFolder, "output.cbz")
                with zipfile.ZipFile(cbz_filename, 'w') as cbz_file:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                file_path = os.path.join(root, file)
                                cbz_file.write(file_path, os.path.relpath(file_path, temp_dir))
            elif exportType.lower() == "folder":
                #Ensure output folder
                for file in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, file)
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        shutil.move(file_path, os.path.join(outputFolder, file))

        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    else:
        print("Specified directory does not exist, Contact Dario")

    
def browseButton(entry):
    filename = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def executeExtraction(input_folder, output_folder, exportType):
    labelMove(input_folder.get(), output_folder.get(), exportType)

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

    compile_to_folder_button = tk.Button(root, text="Compile to Folder", command=lambda: executeExtraction(input_folder_entry, output_folder_entry, "Folder"))
    compile_to_folder_button.grid(row=3, column=1, padx=5, pady=5)

    compile_to_cbz_button = tk.Button(root, text="Compile to CBZ", command=lambda: executeExtraction(input_folder_entry, output_folder_entry, "CBZ"))
    compile_to_cbz_button.grid(row=2, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
