#/usr/bin/python
#encoding:utf-8
import csv
import os
import time

#控制类
class Controller(object):
    def __init__(self, count):
        self.counter = count
        self.alldata = [("timestamp", "cpustatus")]

    #单次测试过程
    def testprocess(self):
        result = os.popen("adb shell dumpsys cpuinfo | grep com.android.browser")
        for line in result.readlines():
            cpuvalue =  line.split("%")[0]

        currenttime = self.getCurrentTime()
        self.alldata.append((currenttime, cpuvalue))

    #多次执行测试过程
    def run(self):
        while self.counter >0:
            self.testprocess()
            self.counter = self.counter - 1
            time.sleep(3)

    #获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    #数据的存储
    def SaveDataToCSV(self):
        csvfile = file('cpustatus.csv', 'wb')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()

if __name__ == "__main__":
    controller = Controller(10)
    controller.run()
    controller.SaveDataToCSV()
