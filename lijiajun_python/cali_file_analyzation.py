import csv
import re
import matplotlib.pyplot as plt


def parse_region_info(input):
    result_list = []
    for i in input:
        result = re.findall('\d+', i)
        result_list.append(int(result[0]))
    return result_list


def parse_wig_info(input):
    phase_list = []
    erro_list = []
    [phase, erro] = input
    for i in phase:
        if i == 'Phase':
            continue
        # result = re.findall(r'\d+\.\d+', i)
        # erro_list.append(float(result[0]))
        phase_list.append(float(i))

    for i in erro:
        if i == 'Erro':
            continue
        # result = re.findall(r'-*\d+\.\d+', i)
        # erro_list.append(float(result[0]))
        erro_list.append(float(i))

    return [phase_list, erro_list]


def parse_wig_csv(file_path):
    result_list = []
    with open(file_path) as csv_file:
        try:
            i = 0
            csv_reader = csv.reader(csv_file)
            for csv_row in csv_reader:
                if i == 1:
                    temp = csv_row[1:4]
                    result_list.append(temp)
                elif i > 1:
                    if i < 5:
                        count = len(csv_row)
                        result_list.append(csv_row[0:count - 1])
                    elif (i - 1) % 4 == 0:
                        count = 3
                        result_list.append(csv_row[0:count])
                    else:
                        count = len(csv_row)
                        result_list.append(csv_row[0:count-1])
                i += 1
        except Exception as err:
            print(err)
    item_count = len(result_list)
    wig_count = item_count // 4
    wig_result = []
    for i in result_list:
        print(i)
    for i in range(0, item_count, 4):
        region_info = parse_region_info(result_list[i])
        wig_info = parse_wig_info([result_list[i+1], result_list[i+2]])
        wig_result.append([region_info, wig_info[0], wig_info[1]])
    return wig_result


def show_wig_pic(wig_array):
    print(len(wig_array))
    for i in wig_array:
        print(i)
    row = 8
    col = 11
    for i in range(row):
        for j in range(col):
            index = i * col + j
            [region, x, y] = wig_array[index]
            ax = plt.subplot(row, col, index+1)
            ax.plot(x, y, label='R%d_x:%d_y:%d' % (region[0], region[1], region[2]))
            ax.scatter(x, y, alpha=0.5, marker='x')
            ax.set_title('R%d_x:%d_y:%d' % (region[0], region[1], region[2]), fontsize=6)
            plt.xticks(fontsize=5)
            plt.yticks(fontsize=5)
    plt.show()


def show_all_map_wig_curve(file_path):
    wig_array = parse_wig_csv(file_path)
    show_wig_pic(wig_array)


if __name__ == '__main__':
    path = r'.\data\floodPureShift.csv'
    show_all_map_wig_curve(path)
