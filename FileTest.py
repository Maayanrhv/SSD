import os

import h5py

# print(os.getcwd())  # get current file directory

origFilePath = "Output\\2020-10-08-13-57-07\\00_FullData_2020-10-08-13-57-07.hdf5"
f = h5py.File(origFilePath, 'r')
print(list(f.keys()))
