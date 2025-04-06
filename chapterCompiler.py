import os
import zipfile
import shutil
import tempfile
import tkinter as tk
from tkinter import filedialog

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

def labelMove(parentFolder, outputFolder, exportType):
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    counter = 1
    temp_dir = tempfile.mkdtemp()

    try:
        for root, dirs, files in os.walk(parentFolder):
            for file in sorted(files):
                file_path = os.path.join(root, file)

                if file.lower().endswith(('.cbz', '.zip')):
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            for member in sorted(zip_ref.namelist()):
                                if member.lower().endswith(SUPPORTED_EXTENSIONS):
                                    try:
                                        with zip_ref.open(member) as source:
                                            new_file_path = os.path.join(temp_dir, f"{counter:03d}.jpg")
                                            with open(new_file_path, "wb") as target:
                                                shutil.copyfileobj(source, target)
                                            counter += 1
                                    except Exception as e:
                                        print(f"Failed to extract {member} from {file}: {e}")
                    except zipfile.BadZipFile:
                        print(f"Error: {file_path} is not a valid zip.")
                    except Exception as e:
                        print(f"An error occurred while processing {file_path}: {e}")

                elif file.lower().endswith(SUPPORTED_EXTENSIONS):
                    new_file_path = os.path.join(temp_dir, f"{counter:03d}.jpg")
                    shutil.copy(file_path, new_file_path)
                    counter += 1

        # Export
        if exportType.lower() == "cbz":
            cbz_filename = os.path.join(outputFolder, "CompiledChapters.cbz")
            with zipfile.ZipFile(cbz_filename, 'w') as cbz_file:
                for root, dirs, files in os.walk(temp_dir):
                    for file in sorted(files):
                        if file.lower().endswith(SUPPORTED_EXTENSIONS):
                            file_path = os.path.join(root, file)
                            cbz_file.write(file_path, os.path.relpath(file_path, temp_dir))

        elif exportType.lower() == "folder":
            for file in sorted(os.listdir(temp_dir)):
                file_path = os.path.join(temp_dir, file)
                if file.lower().endswith(SUPPORTED_EXTENSIONS):
                    shutil.move(file_path, os.path.join(outputFolder, file))

    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def browseButton(entry):
    filename = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def executeExtraction(input_folder, output_folder, exportType, status_label):
    try:
        labelMove(input_folder.get(), output_folder.get(), exportType)
        status_label.config(text="Files compiled successfully!", fg="green")
    except Exception as e:
        print(f"ERROR: {e}")
        status_label.config(text="Something went wrong, contact dev.", fg="red")

    # Auto-clear status message after 5 seconds
    status_label.after(5000, lambda: status_label.config(text=""))

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

    # Status message label
    status_label = tk.Label(root, text="", font=('Arial', 10))
    status_label.grid(row=4, column=1, pady=(0, 5))

    compile_to_cbz_button = tk.Button(root, text="Compile to CBZ", command=lambda: executeExtraction(input_folder_entry, output_folder_entry, "CBZ", status_label))
    compile_to_cbz_button.grid(row=2, column=1, padx=5, pady=5)

    compile_to_folder_button = tk.Button(root, text="Compile to Folder", command=lambda: executeExtraction(input_folder_entry, output_folder_entry, "Folder", status_label))
    compile_to_folder_button.grid(row=3, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
