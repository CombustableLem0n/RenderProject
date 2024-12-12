import os
import subprocess

def convert_dat_from_specific_folders_to_stl_with_ldview(input_folder, output_folder, allowed_folders, ldview_path="ldview"):
    """
    Converts all .dat files from specific folders to .stl files using LDView.

    Args:
        input_folder (str): Path to the base folder containing .dat files.
        output_folder (str): Path to the folder where .stl files will be saved.
        allowed_folders (list): List of full folder paths from which .dat files should be processed.
        ldview_path (str): Path to the LDView executable (default assumes it's in PATH).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Debug: Print the folder structure
    print("Scanning folder structure...")
    for root, dirs, files in os.walk(input_folder):
        print(f"Directory: {root}")
        print(f"Subdirectories: {dirs}")
        print(f"Files: {files}")

    # Collect .dat files only from specific folders
    dat_files = []
    for root, _, files in os.walk(input_folder):
        # Check if the current folder is in the allowed list
        if root in allowed_folders:
            for file_name in files:
                if file_name.endswith(".dat") and not any(x in file_name for x in ["s0", "--", "p0"]):
                    dat_files.append(os.path.join(root, file_name))

    # Collect .dat files only from specific folders, avoiding duplicates
    dat_files = set()  # Use a set to avoid duplicates
    for root, _, files in os.walk(input_folder):
        # Check if the current folder is in the allowed list
        if root in allowed_folders:
            for file_name in files:
                if file_name.endswith(".dat") and not any(x in file_name for x in ["s0", "--", "p0"]):
                    file_path = os.path.join(root, file_name)
                    if file_path not in dat_files:  # Avoid duplicates
                        dat_files.add(file_path)
    
    # Debug: Print the collected files
    print("Collected .dat files:")
    for file in dat_files:
        print(file)

    # Check if any valid files are found
    if not dat_files:
        print("No valid .dat files found in the specified folders.")
        return

    print(f"Found {len(dat_files)} files to convert.")

    # Convert each file
    for file_path in dat_files:
        file_name = os.path.basename(file_path)
        output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".stl")

         # Skip conversion if the .stl file already exists
        if os.path.exists(output_path):
            print(f"Skipping {file_name}: STL already exists.")
            continue

        # Run LDView to convert .dat to .stl
        command = [
            ldview_path,
            file_path,           # Input .dat file
            "-ExportFile=" + output_path,  # Specify the output .stl file with full path
            "-ExportFormat=STL", # Specify export format as STL
            "-AutoCrop",         # Optional: Automatically crop to minimize bounding box
            "-SaveWidth=800",    # Optional: Set rendering width
            "-SaveHeight=600"    # Optional: Set rendering height
        ]
        try:
            print(f"Converting {file_name} to STL...")
            subprocess.run(command, check=True)
            print(f"Saved: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {file_name}: {e}")
        except FileNotFoundError:
            print(f"LDView not found. Ensure it's installed and in your PATH.")

# Example usage
input_folder = r"C:\Users\legol\OneDrive\Desktop\RenderProject\ldraw_collection"
output_folder = r"C:\Users\legol\OneDrive\Desktop\RenderProject\stl_collection"  # Folder to save .stl files
ldview_path = r"C:\Program Files\LDraw (64 Bit)\LDView\LDview64.exe"         # Replace with the full path to LDView if not in PATH

# List of specific folders to process (use full paths)
allowed_folders = [
    r"C:\Users\legol\OneDrive\Desktop\RenderProject\ldraw_complete\LEGO",
    r"C:\Users\legol\OneDrive\Desktop\RenderProject\ldraw_complete\parts",
    r"C:\Users\legol\OneDrive\Desktop\RenderProject\ldraw_complete\UnOfficial\parts"
]

convert_dat_from_specific_folders_to_stl_with_ldview(input_folder, output_folder, allowed_folders, ldview_path=ldview_path)
