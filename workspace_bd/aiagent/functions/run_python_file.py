import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file= os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        result = subprocess.run(command,text=True, capture_output=True, timeout=30, check=False)

        result_message = []

        if result.returncode > 0:
            result_message.append(f"Process exited with code {result.returncode}")

        if not (result.stdout or result.stderr):
            result_message.append("No output produced")

        if result.stdout:
            result_message.append(f"STDOUT: {result.stdout}")

        if result.stderr:
            result_message.append(f"STDERR: {result.stderr}")

        return "\n".join(result_message)

    except Exception as e:
        return(f"Error: {e}")
