from os import listdir
from os.path import isfile, join


def edit_file(filepath):
    with open(filepath) as my_file:
        lines_list = my_file.readlines()

    for i, line in enumerate(lines_list):
        if '-test' not in line:
            continue
        lines_list[i] = line.replace('wegenenverkeer-test.data.vlaanderen.be', 'wegenenverkeer.data.vlaanderen.be')

    with open(filepath, 'w') as my_file:
        new_file_contents = ''.join(lines_list)
        my_file.write(new_file_contents)


if __name__ == '__main__':
    directory_path = r"C:\Users\vlaminda\PycharmProjects\OSLOthema-wegenenverkeer\codelijsten"

    only_ttl_files = [f for f in listdir(directory_path) if isfile(join(directory_path, f)) and f.endswith('.ttl')]

    for file in only_ttl_files:
        edit_file(join(directory_path, file))
