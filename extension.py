import re

def get_extension_id(raw: str) -> str:
    pattern = r'/+'
    return re.split(pattern, raw)[1]


def get_extension_path(extension_id: str) -> str:
    return f"chrome-extension://{extension_id}/home.html#onboarding/welcome"


if __name__ == '__main__':
    filename = "name.txt"

    with open(filename, 'r') as file:
        # Read each line of the file one by one
        line = file.readline()
        while line:
            # Process each line
            print(line.strip())  # Stripping newline characters
            # Read the next line
            line = file.readline()
