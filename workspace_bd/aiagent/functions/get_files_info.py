import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
        "required": ["directory"],
   },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    if directory == ".":
        dir_alias = "current"
    else:
        dir_alias = directory

    results = [f"Result for {dir_alias} directory:"]

    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_contents = os.listdir(target_dir)

        for file in dir_contents:
            file_path = target_dir+"/"+file
            file_size = os.path.getsize(file_path)
            dir_check = os.path.isdir(file_path)
            results.append(f"- {file}: file_size={file_size}, is_dir={dir_check}")

        return "\n".join(results)


    except Exception as e:
        return(f"Error: {e}")
