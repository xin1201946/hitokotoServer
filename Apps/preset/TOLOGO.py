import sys
import cv2


def to_ascii(image_path, grays="@%#*+=-:. ", gs=10):
    img = cv2.imread(image_path, 0)  # 读入灰度图

    # 宽（列）和高（行数）
    w = img.shape[1]
    h = img.shape[1]
    ratio = float(w) / h  # 调整长宽比 (**注：此比例为win cmd，ratio需要根据不同终端的字符长宽调整)

    scale = w // 50  # 缩放尺度，向下取整，每50个像素取一个 值越小图越小(scale 越大)

    for y in range(0, h, int(scale * ratio)):  # 根据缩放长度 遍历高度 y对于h，x对应w
        for x in range(0, w, scale):  # 根据缩放长度 遍历宽度
            idx = img[y][x] * gs // 255  # 获取每个点的灰度  根据不同的灰度填写相应的 替换字符
            if idx == gs:
                idx = gs - 1
            sys.stdout.write(grays[idx])  # 写入控制台
        sys.stdout.write('\n')
        sys.stdout.flush()


def img_RGBcolor_ascii(image_path,r=3):
    # img: input img here is 3channel!
    # r:  raito params #由于不同控制台的字符长宽比不同，所以比例需要适当调整。
    # window cmd：r=3/linux console r=
    img = cv2.imread(image_path, r)
    grays = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^.` "  # 由于控制台是白色背景，所以先密后疏/黑色背景要转置一下
    gs = 67  # 10级灰度
    # grays2 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^.` "
    # gs2 = 67              #67级灰度

    # 宽（列）和高（行数）
    w = img.shape[1]
    h = img.shape[0]
    ratio = r * float(w) / h  # 调整长宽比-根据终端改变r

    scale = w // 100  # 缩放尺度/取值步长，向下取整，每100/50个像素取一个 值越小图越小(scale 越大)

    for y in range(0, h, int(scale * ratio)):  # 根据缩放长度 遍历高度 y对于h，x对应w
        strline = ''
        for x in range(0, w, scale):  # 根据缩放长度 遍历宽度
            idx = int(img[100][100].mean()) * gs // 255  # 获取每个点的灰度  根据不同的灰度填写相应的 替换字符
            if idx == gs:
                idx = gs - 1  # 防止溢出
            ######改变这里，将RGB值，利用2控制参数直接输入
            color_id = "\033[38;2;%d;%d;%dm%s" % (img[y][x][0], img[y][x][1], img[y][x][2], grays[2])  # 输出！
            # 38为前景  ->> 48为背景 ,使用grays[-1/-2]输出
            strline += color_id  # 按行写入控制台
        print(strline)