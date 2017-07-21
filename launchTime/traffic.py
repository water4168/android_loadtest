#/usr/bin/python
#encoding:utf-8
import csv
import os
import string
import time

#控制类
class Controller(object):
    def __init__(self, count):
        #定义测试的次数
        self.counter = count
        #定义收集数据的数组
        self.alldata = [("timestamp", "traffic")]

    #单次测试过程
    def testprocess(self):
        #执行获取进程的命令
        result = os.popen("adb shell ps | grep com.android.browser")
        #获取进程ID
        pid = result.readlines()[0].split(" ")[5]

        #获取进程ID使用的流量
        traffic = os.popen("adb shell cat /proc/"+pid+"/net/dev")
        for line in traffic:
            if "eth0" in line:
                #将所有空行换成#
                line = "#".join(line.split())
                #按#号拆分,获取收到和发出的流量
                receive = line.split("#")[1]
                transmit = line.split("#")[9]
            elif "eth1" in line:
                # 将所有空行换成#
                line =  "#".join(line.split())
                # 按#号拆分,获取收到和发出的流量
                receive2 = line.split("#")[1]
                transmit2 = line.split("#")[9]

        #计算所有流量的之和
        alltraffic = string .atoi(receive) + string .atoi(transmit) + string .atoi(receive2) + string .atoi(transmit2)
        #按KB计算流量值
        alltraffic = alltraffic/1024
        #获取当前时间
        currenttime = self.getCurrentTime()
        #将获取到的数据存到数组中
        self.alldata.append((currenttime, alltraffic))

    #多次测试过程控制
    def run(self):
        while self.counter >0:
            self.testprocess()
            self.counter = self.counter - 1
            #每5秒钟采集一次数据
            time.sleep(5)

    #获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    #数据的存储
    def SaveDataToCSV(self):
        csvfile = file('traffic.csv', 'wb')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()

if __name__ == "__main__":
    controller = Controller(5)
    controller.run()
    controller.SaveDataToCSV()