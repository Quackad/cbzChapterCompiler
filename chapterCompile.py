import os
import zipfile
import argparse 

def labelMove(parent_folder, outputFolder):
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        counter = 1

        if os.path.exists(parent_folder): 
            for root, dirs, files in os.walk(parent_folder):
                    for file in files:
                            if file.lower().endswith('.cbz'):
                                cbz_path = os.path.join(root, file)
                            
                                #CBZ Extraction
                                with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
                                    for member in zip_ref.namelist():
                                        if member.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                            extracted_path = os.path.join(outputFolder, f"{counter:03d}.jpg")
                                            zip_ref.extract(member, outputFolder)
                                            os.rename(os.path.join(outputFolder, member), extracted_path)
                                            counter += 1

        else:
                print("Specified directory does not exist, Contact Dario")

def main():
    parser = argparse.ArgumentParser(description="Extracts images from CBZ files and renames them sequentially.")
    parser.add_argument("inputFolder", help="Parent folder containing CBZ files.")
    parser.add_argument("outputFolder", help="Output folder to place extracted images.")
    args = parser.parse_args()

    labelMove(args.inputFolder, args.outputFolder)

if __name__ == "__main__":
    main()
