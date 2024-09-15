import os

def generate_structure(root_dir, markdown_file, ignore_list):
    def write_tree(dir_path, indent_level=0):
        dir_name = os.path.basename(dir_path)
        # Check if the current directory is in the ignore list
        if dir_name in ignore_list:
            return
        # Write the folder name to the markdown file
        markdown_file.write("  " * indent_level + f"- **{dir_name}/**\n")
        # List the items in the directory, filtering out the ignored files/folders
        for item in sorted(os.listdir(dir_path)):
            item_path = os.path.join(dir_path, item)
            if any(ignored in item_path for ignored in ignore_list):
                continue
            if os.path.isdir(item_path):
                # Recursively write the structure for subdirectories
                write_tree(item_path, indent_level + 1)
            else:
                # Write the file name to the markdown file
                markdown_file.write("  " * (indent_level + 1) + f"- {item}\n")

    write_tree(root_dir)

# Specify the directory and output markdown file name
root_directory = "./"  # Change to your project's root directory
output_file = "folder_structure.md"
ignore_list = [".venv", ".gitignore", "__pycache__", ".git", ".DS_Store", "pycache"]  # Add files and folders to ignore

# Create and write the structure to the markdown file
with open(output_file, 'w') as md_file:
    generate_structure(root_directory, md_file, ignore_list)

print(f"Folder structure has been written to {output_file}")
