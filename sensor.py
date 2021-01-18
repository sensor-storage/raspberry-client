import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "QIypCZDwHiEpUaRe10h1XaOYQbVcvPENWH_84ejDF-pUYSblnEv8RGlrkCaiQfYwEU75rHcN48EIhocGSSoHgg=="
org = "sqy"
bucket = "test"

client = InfluxDBClient(url="http://192.168.0.102:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

makerobo_DO = 17       # 光敏传感器管脚
GPIO.setmode(GPIO.BCM) # 管脚映射，采用BCM编码

# 初始化工作
def makerobo_setup():
    ADC.setup(0x48)      # 设置PCF8591模块地址
    GPIO.setup(makerobo_DO, GPIO.IN) # 光敏传感器，设置为输入模式

# 循环函数
def makerobo_loop():
    makerobo_status = 1 # 状态值
    # 无限循环
    while True:
        v = ADC.read(0)
        print ('Photoresistor Value: ', v) # 读取AIN0的值，获取光敏模拟量值
        point = Point("light").tag("sensor", "sensor1").field("light_intensity", v).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, point)
        time.sleep(0.2)                              # 延时200ms

# 程序入口
if __name__ == '__main__':
    try:
        makerobo_setup() # 地址设置
        makerobo_loop()  # 调用无限循环
    except KeyboardInterrupt: 
        pass    
