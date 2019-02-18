from machine import Pin, I2C, Timer
import ssd1306
import network
import pic_lib
import os
import socket


def delete():
    os.remove('main.py')            # 计时器一启动就烧不进去..只能这样rest之后在烧


def clr(x1, y1, x2, y2):        # 清屏函数 传入xy
    x1 *= 8
    y1 *= 8
    x2 *= 8
    y2 *= 8
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1     # 两点范围容错判断
    y2 += 8
    x2 += 8     # 将判断点移动至右下角
    for y in range(y1, y2):
        for x in range(x1, x2):
            oled.pixel(x, y, 0)


def clr_block(x, y):        # 单字清除
    clr(x, x, y, y)


def clr_line(y):            # 行清除
    clr(0, y, 16, y)


def font_show(strs, x, y):          # 以新坐标显示文字
    oled.text(strs, x * 8, y * 8)


class Block:                            # 顶层图标显示类
    def __init__(self, x, y, data):     # 传入的为8x8后的坐标
        self.x = x * 8                  # 坐标处理为128x64
        self.y = y * 8
        self.data = data * 8

    def show(self):
        for ypods in range(8):
            for xpods in range(7, -1, -1):                                  # 位运算右移后才能销毁数据所以要反过来...
                judge = (pic_lib.icon[ypods + self.data] >> abs(xpods - 7)) & 0x01      # 反过来之后按位移出又要正过来所以用了绝对值...
                if judge:
                    oled.pixel(xpods + self.x, ypods + self.y, 1)
                else:
                    oled.pixel(xpods + self.x, ypods + self.y, 0)

    def hide(self):                                                 # 清除显示
        for ypods in range(8):
            for xpods in range(8):
                oled.pixel(xpods + self.x, ypods + self.y, 0)


def w_check(t):             # 谜之原理 一定要传进一个参数 还没研究
    if wlan.active():
        icon_wifia.show()
    else:
        icon_wifia.hide()

    if wlan.isconnected():
        icon_wific.show()
        oled.text(wlan.ifconfig()[0], 0, 8)
    else:
        icon_wific.hide()
        clr_line(1)

    if ap_if.active():
        icon_ap.show()
    else:
        icon_ap.hide()
    oled.show()


i2c = I2C(scl=Pin(5), sda=Pin(4))  # 创建i2c接口为D1_SCL D2_SDA
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # 创建oled操作对象
wlan = network.WLAN(network.STA_IF) # 连接对象
ap_if = network.WLAN(network.AP_IF) # 热点对象
icon_wifia = Block(0, 0, 0)         # 创建状态图标
icon_wific = Block(1, 0, 1)
icon_ap = Block(2, 0 ,2)
t_wifis = Timer(-1)        # 激活定时器 2hz
t_wifis.init(period=2000, mode=Timer.PERIODIC, callback=w_check)

justgo = socket.socket()
justgo.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        # 基于IPV4 TCP协议 TCP断开后立即释放
justgo.bind(('', 80))
justgo.listen(5)
while True:
    cl, addr = justgo.accept()
    print(cl)
    req = cl.readline()  # 读取第一行
    while True:
        h = cl.readline()  # 读取第二行
        if h == b"" or h == b"\r\n":  # 读取到行尾停止
            break
        # print(h)
        req += (h.decode('utf-8').lower())  # 将每行信息转为小写后保存到req
        # 此时的req为原始数据第一行，和解码后的小写数据
    print("Request")
    req = req.decode('utf-8').lower().split('\r\n')
    # http header 解析
    req_data = req[0].lstrip().rstrip().replace(' ', '')
    print(req_data)
    s = open("s.html")
    cl.send("HTTP/1.1 200 OK\r\n\r\b" + s.read())
    cl.close()
