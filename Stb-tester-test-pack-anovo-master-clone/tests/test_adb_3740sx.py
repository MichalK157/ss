from test_adb import TestADB
from test import Test
import stbt
import time
import datetime

class TestADB3740SX(TestADB):
    
    """ Konstruktor obiektow klasy TestADB3740SX
        argumenty:
            - configPath - sciezka do pliku z parametrami testu dekodera"""
    def __init__(self, configPath, model):
        self.loadConfiguration(configPath, model)

    def sprawdzWyswietlacz():
        Test.runChannel(169)
        print("Czy wyswietalcz swieci poprawnie?")
        print("1) Tak")
        print("2) Nie")
        input = input()
        while input != "1" and input  != "2":
            print("Czy wyswietalcz swieci poprawnie?")
            print("1) Tak")
            print("2) Nie")
            input = input()
        if input == "1":
            self.testsResults["display"] = True
        else:
            self.testsResults["display"] = False

    def sprawdzTimeshifting(self):
        stbt.press("KEY_PAUSE", Test.timeBeforePress)
        try:
            stbt.wait_for_motion(timeout_sec = 3, region = stbt.Region(10, 100, width = 1200, height = 400))
        except MotionTimeout:
            stbt.press("KEY_PLAY", Test.timeBeforePress)
            try:
                stbt.wait_for_motion()
            except MotionTimeout:
                self.testsResults["timeshifting"] = False
            else:
                self.testsResults["timeshifting"] = True
        else:
            self.testsResults["timeshifting"] = False
        stbt.press("KEY_STOP", Test.timeBeforePress)

    def sprawdzHDD(self):
        stbt.press("KEY_REC", Test.timeBeforePress)
        time.sleep(120)
        stbt.press("KEY_STOP", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        stbt.press("KEY_LIST", Test.timeBeforePress)
        today = stbt.ocr(None, stbt.Region(1055, 45, width=80, height=30), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        recordingDate = ocr(None, stbt.Region(660, 200, width=80, height=30), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        if recordingDate == today:
            stbt.press("KEY_PLAY", Test.timeBeforePress)
            time.sleep(10)
            stbt.press("KEY_PAUSE", Test.timeBeforePress)
            try:
                stbt.wait_for_motion(timeout_sec = 3, region = stbt.Region(10, 100, width = 1200, height = 400))
            except MotionTimeout:
                stbt.press("KEY_PLAY", Test.timeBeforePress)
                stbt.press("KEY_FWD", Test.timeBeforePress)
                result = stbt.match_text("x1,5", None, stbt.Region(110, 610, width = 160, height = 30))
                if result:
                    for i in range(3):
                        stbt.press("KEY_REV", Test.timeBeforePress)
                    result = stbt.match_text("x2,0", None, stbt.Region(110, 610, width = 160, height = 30))
                    if result:
                        selft.testsResults["hdd"] = True
                    else:
                        self.testsResults["hdd"] = False
                else:
                    self.testsResults["hdd"] = False
            else:
                self.testsResults["hdd"] = False
            stbt.press("KEY_STOP", Test.timeBeforePress)
            stbt.press("KEY_RED", Test.timeBeforePress)
            stbt.press("KEY_LEFT", Test.timeBeforePress)
            stbt.press("KEY_OK", Test.timeBeforePress)
        else:
            self.testsResults["hdd"] = False
        stbt.press("KEY_LIST", Test.timeBeforePress)
