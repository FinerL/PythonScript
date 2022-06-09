import math
import matplotlib.pyplot as plt
import numpy as np


class coordinate:
    def __init__(self):
        self.x = 0
        self.y = 0

    def setXY(self, _x, _y):
        self.x = _x
        self.y = _y


def create_bazier_curve(ctrl_points, steps):
    nodes = []
    for i in range(steps):
        u = i / steps
        new_ctrl_point = coordinate()
        new_ctrl_point.x = math.pow(u, 3) * (-1 * ctrl_points[0].x + 3 * ctrl_points[1].x - 3 * ctrl_points[2].x + ctrl_points[3].x)
        new_ctrl_point.y = math.pow(u, 3) * (-1 * ctrl_points[0].y + 3 * ctrl_points[1].y - 3 * ctrl_points[2].y + ctrl_points[3].y)
        new_ctrl_point.x += math.pow(u, 2) * (3 * ctrl_points[0].x - 6 * ctrl_points[1].x + 3 * ctrl_points[2].x)
        new_ctrl_point.y += math.pow(u, 2) * (3 * ctrl_points[0].y - 6 * ctrl_points[1].y + 3 * ctrl_points[2].y)
        new_ctrl_point.x += u * (-3 * ctrl_points[0].x + 3 * ctrl_points[1].x)
        new_ctrl_point.y += u * (-3 * ctrl_points[0].y + 3 * ctrl_points[1].y)
        new_ctrl_point.x += ctrl_points[0].x
        new_ctrl_point.y += ctrl_points[0].y
        nodes.append(new_ctrl_point)
    return nodes


def create_sample_points(path):
    with open(path, 'r') as f:
        file = f.readlines()
    i = 0
    for line in file:
        if i is 0:
            phase = line.split(' ')
        if i is 1:
            erro = line.split(' ')
        i += 1
    sample_cnt = len(phase)
    ctrl_points = []
    for cnt in range(sample_cnt):
        ctrl_point = coordinate()
        ctrl_point.setXY(float(phase[cnt]), float(erro[cnt]))
        ctrl_points.append(ctrl_point)
    return ctrl_points


def generate_bazier_nodes(points):
    arr_len = len(points)
    bazier_ctrl_points = []
    for i in range(arr_len - 1):
        x0 = 0
        y0 = 0
        x1 = points[i].x
        y1 = points[i].y
        x2 = points[i+1].x
        y2 = points[i+1].y
        x3 = 0
        y3 = 0
        if i == 0:
            x0 = x1
            y0 = y1
        else:
            x0 = points[i - 1].x
            y0 = points[i - 1].y

        if i == arr_len-2:
            x3 = points[i+1].x
            y3 = points[i+1].y
        else:
            x3 = points[i+2].x
            y3 = points[i+2].y
        x_center_1 = (x0+x1)*0.5
        y_center_1 = (y0+y1)*0.5
        x_center_2 = (x1+x2)*0.5
        y_center_2 = (y1+y2)*0.5
        x_center_3 = (x2+x3)*0.5
        y_center_3 = (y2+y3)*0.5

        linear_len_1 = 0
        linear_len_2 = 0
        linear_len_3 = 0
        temp = (x1-x0)*(x1-x0)+(y1-y0)*(y1-y0)

        if temp>0:
            linear_len_1 = math.sqrt(temp)
        temp = (x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)
        if temp>0:
            linear_len_2 = math.sqrt(temp)
        temp = (x3-x2)*(x3-x2)+(y3-y2)*(y3-y2)
        if temp>0:
            linear_len_3 = math.sqrt(temp)

        k1 = linear_len_1 / (linear_len_1 + linear_len_2)
        k2 = linear_len_2 / (linear_len_2 + linear_len_3)

        x_m_1 = x_center_1 + (x_center_2 - x_center_1)*k1
        y_m_1 = y_center_1 + (y_center_2 - y_center_1)*k1
        x_m_2 = x_center_2 + (x_center_3 - x_center_2)*k2
        y_m_2 = y_center_2 + (y_center_3 - y_center_2)*k2

        x_ctrl_1 = x_center_2 + x1 - x_m_1
        y_ctrl_1 = y_center_2 + y1 - y_m_1
        x_ctrl_2 = x_center_2 + x2 - x_m_2
        y_ctrl_2 = y_center_2 + y2 - y_m_2

        bazier_ctrl_point1 = coordinate()
        bazier_ctrl_point1.setXY(x1, y1)
        if i == 0:
            bazier_ctrl_point2 = coordinate()
            bazier_ctrl_point2.setXY(x1, y1)
        else:
            bazier_ctrl_point2 = coordinate()
            bazier_ctrl_point2.setXY(x_ctrl_1, y_ctrl_1)
        if i == arr_len - 2:
            bazier_ctrl_point3 = coordinate()
            bazier_ctrl_point3.setXY(x2, y2)
        else:
            bazier_ctrl_point3 = coordinate()
            bazier_ctrl_point3.setXY(x_ctrl_2, y_ctrl_2)
        bazier_ctrl_point4 = coordinate()
        bazier_ctrl_point4.setXY(x2, y2)
        bazier_ctrl_points.append(bazier_ctrl_point1)
        bazier_ctrl_points.append(bazier_ctrl_point2)
        bazier_ctrl_points.append(bazier_ctrl_point3)
        bazier_ctrl_points.append(bazier_ctrl_point4)
    return bazier_ctrl_points


def generate_bazier_curve(ctrl_points, interp_cnt):
    per_cnt = (int)(interp_cnt / (len(ctrl_points) / 4))
    curve = []
    for i in range((int)(len(ctrl_points) / 4)):
        i *= 4
        per_ctrl_points = ctrl_points[i:i+4]
        per_curve = create_bazier_curve(per_ctrl_points, per_cnt)
        curve.extend(per_curve)
    return curve


if __name__ == '__main__':
    cali_path = r'.\data\_flood.txt'
    samp_points = create_sample_points(cali_path)
    bazier_nodes = generate_bazier_nodes(samp_points)
    bazier_curve = generate_bazier_curve(bazier_nodes, 300)

    x_before = []
    y_before = []
    x_after = []
    y_after = []
    x_after_bazier = []
    y_after_bazier = []

    for i in range(len(samp_points)):
        x_before.append(samp_points[i].x)
        y_before.append(samp_points[i].y)

    for i in range(len(bazier_nodes)):
        x_after.append(bazier_nodes[i].x)
        y_after.append(bazier_nodes[i].y)

    for i in range(len(bazier_curve)):
        x_after_bazier.append(bazier_curve[i].x)
        y_after_bazier.append(bazier_curve[i].y)

    plt.figure()
    plt.subplot(131)
    plt.scatter(x_before, y_before, c='b')
    plt.subplot(132)
    plt.scatter(x_after, y_after, c='r')
    plt.subplot(133)
    plt.scatter(x_after_bazier, y_after_bazier, c='y')
    plt.show()