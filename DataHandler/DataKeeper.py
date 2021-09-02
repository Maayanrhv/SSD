import csv
import os


def save_diff_to_csv(data, name):
    list_data = data.copy()
    list_data.insert(0, "diff")

    mat = [p for p in zip(list_data)]
    create_csv(mat, name)


def save_with_and_without_sound_to_csv(data1, data2, name):
        list1 = data1.copy()
        list2 = data2.copy()
        list1.insert(0, "With sound")
        list2.insert(0, "Without sound")

        mat = [p for p in zip(list1, list2)]
        create_csv(mat, name)


def create_csv(mat, name):
    csv_name = '{}.csv'.format(name)
    parent_directory = os.path.split(os.getcwd())[0]
    dir_path = os.path.join(parent_directory, "DataFiles")
    csv_path = os.path.join(dir_path, csv_name)

    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(mat)
