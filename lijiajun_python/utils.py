import numpy as np
import matplotlib.pyplot as plt
import matplotlib as cm
import csv
import os
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import struct


def load_csv(file_name, row, col, dataType):
    matrix = np.zeros([row, col], dataType)
    with open(file_name, errors='ignore') as csv_file:
        try:
            i = 0
            csv_reader = csv.reader(csv_file)
            for csv_row in csv_reader:
                matrix[i, :] = list(map(dataType, csv_row[0:col]))
                i = i + 1
                if i == row:
                    break
        except Exception as erro:
            print(erro)
    return matrix


def load_csv_array_from_dir(dir_name, file_suffix, row, col, dataType):
    csv_list = []
    file_list = os.listdir(dir_name)
    for file in file_list:
        if file.endswith(file_suffix):
            csv_list.append(file)
    csv_list.sort()
    rawdata_set = np.zeros([row, col, len(csv_list)], dataType)
    index = 0
    for file in csv_list:
        rawdata_set[:, :, index] = load_csv(dir_name+file, row, col, dataType)
        index += 1
    return rawdata_set


def load_bin(file_name, row, col):
    matrix = np.zeros([row, col]. np.int32)
    with open(file_name, 'rb') as bin_file:
        data = struct.unpack('h' * row * col, bin_file.read(2 * row * col))
        matrix = np.array(data).reshape(row, col)
        bin_file.close()
    return matrix


def load_bin_data(file_name, row, col):
    with open(file_name, 'rb') as bin_file:
        bin_data = []
        for i in range(row * col):
            two_byte = bin_file.read(2)
            data = struct.unpack('h', two_byte)
            bin_data.append(data)
        bin_data_matrix = np.asarray(bin_data)
        bin_data_matrix = bin_data_matrix.reshape(row, col)
        bin_file.close()
    return bin_data_matrix


def load_bin_array_from_dir(dir_name, row, col, file_suffix):
    bin_list = []
    file_list = os.listdir(dir_name)
    for file in file_list:
        if file.endswith(file_suffix):
            bin_list.append(file)
    bin_list.sort()
    rawdata_set = np.zeros([row, col, len(bin_list)], np.int32)
    index = 0
    for file in bin_list:
        rawdata_set[:, :, index] = load_csv(dir_name+file, row, col)
        index += 1
    return rawdata_set


def save_data_to_csv(data, file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    fd = open(file_name, 'w', newline='')
    csv_writer = csv.writer(fd, dialect='excel')
    [row, col] = np.shape(data)
    for i in range(row):
        csv_writer.writerow(data[i])