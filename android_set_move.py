#/usr/bin/python
#encoding:utf-8
'''
每次上传各大应用市场，都要加固打包二十多个apk!
这个脚本自动化了 安装/打开运行/卸载的动作！
后面再加上多进程，实现locat,高效跑动！
'''
import csv
import os
import time


class App(object):
    def __init__(self):
        self.content = ""
        self.startTime = 0


    #开始日志记录
    def StartLog(self):
        cmd = r'adb logcat -v  threadtime> c:/setup_remove.log'
        os.popen(cmd)


    #安装APP
    def InstallApp(self, pname):
        cmd = r'adb install C:\apps\%s'%(pname)
        os.popen(cmd)



    #启动App
    def LaunchApp(self):
        cmd = r'adb shell am start -W -n com.pingan.mc.offical.distribution/com.pingan.mc.offical.appstart.SplishAcitvity'
        self.content=os.popen(cmd)

    #停止App
    def StopApp(self):
        #cmd = 'adb shell am force-stop com.android.browser'
        cmd = 'adb shell input keyevent 3'
        os.popen(cmd)


    #卸载app
    def RemoveApp(self):
        cmd = 'adb uninstall com.pingan.mc.offical.distribution'
        self.content=os.popen(cmd)


#控制类
class Controller(object):
    def __init__(self):
        self.app = App()


    #执行一条龙服务，日志/遍历文件/安装/运行/卸载
    def run(self, dirpath):
        
        for root, dirs, apps in os.walk(dirpath):
            for app_name in apps:

                print app_name

                self.app.InstallApp(app_name)

                time.sleep(3)

                self.app.LaunchApp()

                time.sleep(15)

                self.app.RemoveApp()


if __name__ == "__main__":
    controller = Controller()
    dirpath = "c:/apps"
    controller.run(dirpath)
