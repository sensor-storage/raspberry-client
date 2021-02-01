import os
import time
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "QIypCZDwHiEpUaRe10h1XaOYQbVcvPENWH_84ejDF-pUYSblnEv8RGlrkCaiQfYwEU75rHcN48EIhocGSSoHgg=="
org = "sqy"
bucket = "test"

client = InfluxDBClient(url="http://192.168.0.102:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

makerobo_ds18b20 = ''  # ds18b20 设备


def makerobo_setup():
    global makerobo_ds18b20  # 全局变量
    # 获取 ds18b20 地址
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            makerobo_ds18b20 = i  # ds18b20存放在ds18b20地址


# 读取ds18b20地址数据
def makerobo_read():
    makerobo_location = '/sys/bus/w1/devices/' + makerobo_ds18b20 + '/w1_slave'  # 保存ds18b20地址信息
    makerobo_tfile = open(makerobo_location)  # 打开ds18b20
    makerobo_text = makerobo_tfile.read()  # 读取到温度值
    makerobo_tfile.close()  # 关闭读取
    secondline = makerobo_text.split("\n")[1]  # 格式化处理
    temperaturedata = secondline.split(" ")[9]  # 获取温度数据
    temperature = float(temperaturedata[2:])  # 去掉前两位
    temperature = temperature / 1000  # 去掉小数点
    return temperature  # 返回温度值


# 循环函数
def makerobo_loop():
    while True:
        if makerobo_read() != None:  # 调用读取温度值，如果读到到温度值不为空
            v = makerobo_read()
            print("Current temperature : %0.3f C" % v)  # 打印温度值
            point = Point("temperature").tag("sensor", "sensor1").field("temp", v).time(datetime.utcnow(),
                                                                                       WritePrecision.NS)
            write_api.write(bucket, org, point)
            time.sleep(0.2)  # 延时200ms


# 释放资源
def destroy():
    pass


# 程序入口
if __name__ == '__main__':
    try:
        makerobo_setup()  # 调用初始化程序
        makerobo_loop()  # 调用循环函数
    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
        destroy()  # 释放资源
