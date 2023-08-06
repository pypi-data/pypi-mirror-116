import pandas as pd
import numpy as np
import glob, os
from tabulate import tabulate
import pkg_resources

class Data():
    def __init__(self):
        self.data = None
        self.target = None

def get_dataset(dataset_name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    data_paths = pkg_resources.resource_listdir('Py_FS.datasets','database')
    # print("Package Paths:", data_paths)
    list_datasets = [os.path.splitext(os.path.basename(filename))[0] for filename in data_paths]

    # print(dir_name)

    if dataset_name not in list_datasets:
        print(f"[!Error] Py_FS currently does not have {dataset_name} in its database....")
        display = input("Enter 1 to see the available datasets: ") or 0
        if display:
            display_datasets(list_datasets)

    else:
        data = Data()
        stream = pkg_resources.resource_stream(__name__, 'database/' + dataset_name + '.csv')
        df = pd.read_csv(stream, header=None)
        data.data = np.array(df.iloc[:, 0:-1])
        data.target = np.array(df.iloc[:, -1])

        print(data.data.shape)
        print(data.target.shape)


def display_datasets(list_datasets):
    print("\n=========== Available Datasets ===========\n")
    table_list = []

    for i, dataset in enumerate(list_datasets):
        table_list.append([i+1, list_datasets[i]])

    print(tabulate(table_list, headers=["Index", "Dataset"]))

if __name__ == '__main__':
    get_dataset('Vow')
