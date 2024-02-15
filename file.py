def read_line(filename: str) -> list[str]:
    item_list = []
    with open(filename, 'r') as file:
        # Read each line of the file one by one
        line = file.readline()
        while line:
            item_list.append(line.strip())
            line = file.readline()

    return item_list


def write_line(data: list[str], filename: str) -> None:
    with open(filename, 'w') as file:
        for line in data:
            file.write(line + '\n')


if __name__ == '__main__':
    print(len(read_line("export.txt")))
