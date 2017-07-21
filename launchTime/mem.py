#/usr/bin/python
#encoding:utf-8
import csv
import os
import  time

#控制类
class Controller(object):
    def __init__(self):
        #定义收集数据的数组
        self.alldata = [("id", "vss", "rss")]

    #分析数据
    def analyzedata(self):
        content = self.readfile()
        i = 0
        for line in content:
            if "com.android.browser" in line:
                print line
                line = "#".join(line.split())
                vss = line.split("#")[5].strip("K")
                rss = line.split("#")[6].strip("K")

                #将获取到的数据存到数组中
                self.alldata.append((i, vss, rss))
                i = i + 1

    #数据的存储
    def SaveDataToCSV(self):
        csvfile = file('meminfo.csv', 'wb')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()

    #读取数据文件
    def readfile(self):
        mfile = file("meminfo", "r")
        content = mfile.readlines()
        mfile.close()
        return  content

if __name__ == "__main__":
    controller = Controller()
    controller.analyzedata()
    controller.SaveDataToCSV()