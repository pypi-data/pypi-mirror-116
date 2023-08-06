from time import time
from datetime import datetime, timedelta
from xml.parsers.expat import ExpatError
from ..tools import sleep
from ..multi import runThreadsWithArgsList, threadLock
from .project import Project


class Activity:
    SplashActivity = 'com.ss.android.ugc.aweme.lite/com.ss.android.ugc.aweme.splash.SplashActivity'  # 抖音极速版程序入口


class Text:
    iKnow = '我知道了'  # 儿童/青少年模式提醒


class ResourceID:
    av0 = 'com.ss.android.ugc.aweme.lite:id/av0'  # 关闭（12个红包 超多现金福利）
    bai = 'com.ss.android.ugc.aweme.lite:id/bai'  # 关闭（邀请5个好友必赚136元/恭喜你被红包砸中）
    bc1 = 'com.ss.android.ugc.aweme.lite:id/bc1'  # 开红包（恭喜你被红包砸中）
    e0p = 'com.ss.android.ugc.aweme.lite:id/e0p'  # 暂时不要（发现通讯录好友）


class DYJSB(Project):
    def __init__(self, deviceSN):
        super(DYJSB, self).__init__(deviceSN)
        self.startDay = datetime.now().day

    def openApp(self):
        super(DYJSB, self).openApp(Activity.SplashActivity)
        sleep(30)
        try:
            if self.uIAIns.click(text=Text.iKnow):
                sleep(3)
                self.uIAIns.xml = ''
            if self.uIAIns.click(ResourceID.av0, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click(ResourceID.bai, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            self.uIAIns.click(ResourceID.e0p, xml=self.uIAIns.xml)
        except (FileNotFoundError, ExpatError) as e:
            print(e)

    def randomSwipe(self, initRestTime=False):
        super(DYJSB, self).randomSwipe(530, 560, 530, 560, 1160, 1190, 360, 390, initRestTime)

    def watchVideo(self):
        if datetime.now().hour > 22 or datetime.now().hour < 7:
            if datetime.now().hour == 23 and datetime.now().day == self.startDay:
                self.freeMemory()
                self.adbIns.pressPowerKey()
                self.startDay = (datetime.now() + timedelta(days=1)).day
            return
        try:
            if self.uIAIns.click(ResourceID.bc1):
                self.uIAIns.click(ResourceID.bai, xml=self.uIAIns.xml)
        except (FileNotFoundError, ExpatError) as e:
            print(e)
        if self.reopenAppPerHour():
            self.adbIns.keepOnline()
        # if Activity.SplashActivity not in self.adbIns.getCurrentFocus():
        #     self.reopenApp()
        self.restTime = self.restTime + self.lastTime - time()
        self.lastTime = time()
        self.randomSwipe()

    @classmethod
    def mainloop(cls, devicesSN):
        runThreadsWithArgsList(cls, devicesSN)
        while True:
            for i in cls.instances:
                i.watchVideo()
            print('现在是', datetime.now(), '，已运行：', datetime.now() - cls.startTime,
                  sep='', end='\n\n')
