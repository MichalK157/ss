from test import Test
import stbt

class TestHDS(Test):
    model = ""
    mainTerrestrialTestChannel = 0
    alternativeTerrestrialTestChannel = 0

    def __init__(self, model, configPath):
        self.model = model
        self.loadConfiguration(configPath, model)

    def testFuncjonalny(self):
        scanedSN #zeskanowany SN dekodera
        self.sprawdzSN(scannedSN)
        stbt.press("KEY_MENU", self.timeBeforePress)
        try:
            stbt.wait_for_motion(90)
        except stbt.MotionTimeout:
            pass
        self.sprawdzCzytnikKart()
        stbt.press("KEY_REC", self.timeBeforePress)
        self.testKanalow()
        self.sprawdzUSB()
        self.sprawdzTimeshifting()
        stbt.press("KEY_MENU", self.timeBeforePress)
        stbt.press("KEY_LEFT", self.timeBeforePress)
        stbt.press("KEY_LEFT", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        self.sprawdzRachunki()
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_MENU", self.timeBeforePress)
        self.myPressUntilMatchText("WIADOMOSCI", "KEY_LEFT", stbt.Region(x=550, y=605, width=180, height=41), 10)
        stbt.press("KEY_OK", self.timeBeforePress)
        self.sprawdzWiadomosci()
        stbt.press("KEY_EXIT", self.timeBeforePress)
        stbt.press("KEY_STOP", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_RIGHT", self.timeBeforePress)
        stbt.press("KEY_RIGHT", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        self.sprawdzHDD()
        self.wejdzWUstawienia()
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_DOWN", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        self.sprawdzMaxIndex()
        stbt.press("KEY_EXIT",self.timeBeforePress)
        self.wejdzWUstawienia()
        stbt.press("KEY_DOWN", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_4", self.timeBeforePress)
        stbt.press("KEY_3", self.timeBeforePress)
        self.sprawdzSiec()
        stbt.press("KEY_EXIT", self.timeBeforePress)
        self.wejdzWUstawienia()
        stbt.press("KEY_DOWN", self.timeBeforePress)
        stbt.press("KEY_7", self.timeBeforePress)
        stbt.press("KEY_2", self.timeBeforePress)
        self.sprawdzWersjeOprogramowania()        
        stbt.press("KEY_A", self.timeBeforePress)
        stbt.press("KEY_1", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        self.sprawdzSileIJakosSygnalu()
        stbt.press("KEY_EXIT", self.timeBeforePress)
        self.sprawdzWyswietlacz()
        if self.model = "HDS7241/91":
            self.sprawdzTVNaziemna()
        self.sprawdzPrzyciski()

    def testAutodiag(self):
        scanedSN #zeskanowany SN dekodera
        self.sprawdzSN(scannedSN)
        stbt.press("KEY_OK", Test.timeBeforePress)
        for i in range(10):
            result = stbt.match_text("OK", None, stbt.Region(x=665, y=293 + 16 * i, width=30, height=16))
            if result == False:
                self.testsResults["hds_autodiag_hardware_test"] = False
                return
        stbt.prsss("KEY_DOWN", Test.timeBeforePress)
        for i in range(3):
            result = stbt.match_text("OK", None, stbt.Region(x=665, y=293 + 16 * i, width=30, height=16))
            if result == False:
                self.testsResults["hds_autodiag_hardware_test"] = False
                return
        stbt.press("KEY_MENU",  Test.timeBeforePress)
        stbt.press_until_match("KEY_DOWN", "./images/t1/hds_hard_disk.png", self.timeBeforePress, 5, region = stbt.Region(x=464, y=357, width=117, height=13))
        stbt.press("KEY_OK", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        result = stbt.match_text("PASS")
        if result == False:
            self.testsResults["hdd"] = False
            return
        stbt.press("KEY_MENU",  Test.timeBeforePress)
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        while True:
            time.sleep(2)
            if stbt.match_text("PASS", region = stbt.Region(x=663, y=290, width=70, height=20)):
                self.testsResults["hdd"] = True
                break
            elif stbt.match_text("FAIL", region = stbt.Region(x=663, y=290, width=70, height=20)):
                self.testsResults["hdd"] = False
                return
        stbt.press("KEY_MENU", Test.timeBeforePress)
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        self.typeAutodiagPassword()
        while True:
            time.sleep(2)
            if stbt.match_text("PASS", region = stbt.Region(x=663, y=290, width=70, height=20)):
                self.testsResults["hdd"] = True
                break
            elif stbt.match_text("FAIL", region = stbt.Region(x=663, y=290, width=70, height=20)):
                self.testsResults["hdd"] = False
                return
        stbt.press("KEY_MENU", Test.timeBeforePress)
        stbt.press("KEY_MENU", Test.timeBeforePress)
        stbt.press_until_match("KEY_DOWN", "./images/t1/hds_autodiag_factory_settings.png", Test.timeBeforePress, 5, region = stbt.Region(x=464, y=371, width=212, height=21))
        stbt.press("KEY_OK", Test.timeBeforePress)
        self.typeAutodiagPassword()
        stbt.press("KEY_OK", Test.timeBeforePress)
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        while True:
            time.sleep(2)
            if stbt.match_text("DONE", region = stbt.Region(x=637, y=292, width=78, height=14))):
                while True:
                    time.sleep(1)
                    if stbt.match_text("DONE", region = stbt.Region(x=636, y=309, width=70, height=14):
                        self.testsResults["hds_factory_settings"] = True
                        break
                    elif stbt.match_text("FAIL", region = stbt.Region(x=636, y=309, width=70, height=14):
                        self.testsResults["hds_factory_settings"] = False
                        return
                break
            elif stbt.match_text("FAIL", region = stbt.Region(x=637, y=292, width=78, height=14)):
                self.testsResults["hds_factory_settings"] = False
                return
        stbt.press("KEY_MENU", Test.timeBeforePress)
        stbt.press("KEY_MENU", Test.timeBeforePress)

    def wejdzWUstawienia(self):
        stbt.press("KEY_MENU", self.timeBeforePress)
        self.myPressUntilMatchText("USTAWIENIA", "KEY_RIGHT", stbt.Region(x=550, y=605, width=180, height=41), 10)
        stbt.press("KEY_OK", self.timeBeforePress)

    def typeAutodiagPassword(self):
        stbt.press("KEY_5", Test.timeBeforePress)
        stbt.press("KEY_5", Test.timeBeforePress)
        stbt.press("KEY_5", Test.timeBeforePress)

    def sprawdzRachunki(self):
        result = stbt.match_text("BRAK", None, stbt.Region(x=845, y=235, width=72, height=26))
        if result:
            self.testsResults["bills"] = True
        else:
            self.testsResults["bills"] = False

    def sprawdzWiadomosci(self):
        result = stbt.ocr(region = stbt.Region(x=101, y=135, width=1075, height=32))
        if result == "":
            self.testsResults["messages"] = True
        else:
            self.testsResults["messages"] = False

    def sprawdzHDD(self):
        today = stbt.ocr(region = stbt.Region(x=1026, y=35, width=86, height=33))
        recordingDate = ocr(region = stbt.Region(x=673, y=543, width=62, height=22))
        if recordingDate == today:
            stbt.press("KEY_PLAY", Test.timeBeforePress)
            time.sleep(10)
            stbt.press("KEY_PAUSE", Test.timeBeforePress)
            try:
                stbt.wait_for_motion(timeout_sec = 3, region = stbt.Region(x=10, y=11, width=1260, height=540))
            except MotionTimeout:
                stbt.press("KEY_REV", Test.timeBeforePress)
                if stbt.match_text("x4", region = stbt.Region(x=186, y=588, width=30, height=21)):
                    stbt.press("KEY_FWD", Test.timeBeforePress)
                    stbt.press("KEY_FWD", Test.timeBeforePress)
                    if stbt.match_text("x8", region = stbt.Region(x=186, y=588, width=30, height=21)):
                        selft.testsResults["hdd"] = True
                    else:
                        self.testsResults["hdd"] = False
                else:
                    self.testsResults["hdd"] = False
            else:
                self.testsResults["hdd"] = False
            stbt.press("KEY_STOP", Test.timeBeforePress)
            stbt.press("KEY_3", Test.timeBeforePress)
            stbt.press("KEY_OK", Test.timeBeforePress)
        else:
            self.testsResults["hdd"] = False

    def sprawdzSN(self, scannedSN):
        SN = stbt.ocr(region = stbt.Region(x=600, y=251, width=164, height=19))
        print("Odczytany SN: ", SN)  
        if SN != scannedSN:
            self.testsResults["sn"] = False
        else:
            self.testsResults["sn"] = True

    def sprawdzCzytnikKart(self):
        print("Wloz karte do czytnika.")
        result = myWaitWhileMatchText("BRAK KARTY", stbt.Region(x=555, y=127, width=165, height=33))
        if result:
            result = stbt.match("./images/t1/hds_smart_card_error.png", region = stbt.Region(x=555, y=127, width=165, height=33))
            if result:
                self.testsResults["card_reader"] = False
            else:
                self.testsResults["card_reader"] = True
        else:
            self.testsResults["card_reader"] = False

    def sprawdzMaxIndex(self):
        maxIndex = stbt.ocr(region = stbt.Region(x=669, y=418, width=56, height=35)) #stbt.ocr(None, stbt.Region(x=669, y=418, width=56, height=35), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        if maxIndex == "0":
            self.testsResults["max_index"] = True
        else:
            self.testsResults["max_index"] = False

    def sprawdzSiec(self):
        ipTestResult = stbt.match_text("172.16", None, stbt.Region(x=655, y=233, width=56, height=24))
        if  ipTestResult == False:
            self.testsResults["ethernet"] = False
        else:
            self.testsResults["ethernet"] = True

    def sprawdzWersjeOprogramowania(self):
        softVersion = stbt.ocr(region = stbt.Region(x=811, y=323, width=47, height=21)) #stbt.ocr(None, stbt.Region(x=811, y=323, width=47, height=21), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        if softVersion == currentUpdateVersions[0]uv or softVersion == currentUpdateVersions[1]:
            self.testsResults["soft_version"] = True
        else:
            self.testsResults["soft_version"] = False

    def sprawdzSileIJakosSygnalu(self):
        self.testsResults["signal_level"] = stbt.match("./images/t1/hds_signal_level.png", region = stbt.Region(x=743, y=324, width=111, height=19))

    def sprawdzUSB(self, port):
        print("Wloz Pendrive do gniazda USB umieszczonego z boku.")
        input = input("Czy dioda Pendrive swieci?\n1) Tak\n2) Nie")
        while input != "1" and input  != "2":
            input = input("Czy dioda Pendrive swieci?\n1) Tak\n2) Nie")
        if input == "1":
            self.testsResults[port] = True
        else:
            self.testsResults[port] = False

    def sprawdzTimeshifting(self):
        stbt.press("KEY_PAUSE", Test.timeBeforePress)
        try:
            stbt.wait_for_motion(timeout_sec = 3, region = stbt.Region(x=10, y=70, width=1260, height=480))
        except MotionTimeout:
            stbt.press("KEY_STOP", Test.timeBeforePress)
            try:
                stbt.wait_for_motion()
            except MotionTimeout:
                self.testsResults["timeshifting"] = False
            else:
                self.testsResults["timeshifting"] = True
        else:
            self.testsResults["timeshifting"] = False

    def sprawdzWyswietlacz(self):
        self.runChannel("888")
        input = input("Czy wyswietlacz swieci prawidlowo?\n1) Tak\n2) Nie")
        while input != "1" and input  != "2":
            input = input("Czy wyswietlacz swieci prawidlowo?\n1) Tak\n2) Nie")
        if input == "1":
            self.testsResults["display"] = True
        else
            self.testsResults["dispaly"] = False

    def sprawdzTVNaziemna(self):
        self.runChannel("998")
        input = input("Czy obraz na ekranie wyswietlany jest prawidlowo?\n1) Tak\n2) Nie")
        while input != "1" and input != "2":
            input = input("Czy obraz na ekranie wyswietlany jest prawidlowo?\n1) Tak\n2) Nie")
        if input == "1":
            self.testsResults["terrestrial_siganl_quality"] = True
        else:
            self.runChannel("994")
            input = input("Czy obraz na ekranie wyswietlany jest prawidlowo?\n1) Tak\n2) Nie")
            while input != "1" and input != "2":
                input = input("Czy obraz na ekranie wyswietlany jest prawidlowo?\n1) Tak\n2) Nie")
            if input == "1":
                self.testsResults["terrestrial_siganl_quality"] = True
            else:
                self.testsResults["terrestrial_siganl_quality"] = False
    
    def sprawdzPrzyciski(self, maxAttempts = 5):
        result = {}
        counter = 0
        print("Wcisnij kalwisz P-")
        detection = channelSwitchDetection(self.mainTestChannels[0])
        while detection[0] != 1 and counter < maxAttempts:
            detection = channelSwitchDetection(self.mainTestChannels[0])
            counter += 1
        if counter == maxAttempts:
            result["P-"] = False
        else:
            result["P-"] = True
        time.sleep(5)
        print("Wciśnij klawisz 'P+'")
        counter = 0
        detection = channelSwitchDetection(detection[1])
        while detection[0] != 2 and counter < maxAttempts:
            detection = channelSwitchDetection(detection[1])
            counter += 1
        if counter == maxAttempts:
            result["P+"] = False
        else:
            result["P+"] = True
        
        print("Wcisnij klawisz 'V+'")
        result["V+"] = self.volumeUpSwitchDetection()

        print("Wcisnij klawisz 'V-'")
        result["V-"] = self.volumeDownSwitchDetection()

        time.sleep(5)
        print("Wcisnij klawisz 'St-By'")
        counter = 0
        detection = stbySwitchDetection()
        while detection == False and counter < maxAttempts:
            detection = stbySwitchDetection()
            counter += 1
        if counter == maxAttempts:
            result["St-By"] = False
        else:
            result["St-By"] = True

        self.testsResults["switches"] = result

    def channelSwitchDetection(channelToCompare):
        result = [0, 0]
        try:
            stbt.wait_for_match("./images/t1/hds_up_arrow.png", region = stbt.Region(x=255, y=539, width=39, height=31)) # oczekiwanie na wcisnienie przycisku
        except stbt.MatchTimeout:
            result[0] = -1
            result[1] = channelToCompare
            return result
        channelNumber = stbt.ocr(None, stbt.Region(90, 592, width=45, height=41), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        cn = int(channelNumber)
        result[1] = cn
        if cn < channelToCompare:
            result[0] = 1
        elif cn > channelToCompare:
            result[0] = 2
        return result

    def stbySwitchDetection(maxAttempts = 5, sleepTime = 1):
        counter = 0
        result = stbt.is_screen_black()
        while result.black == False and counter <= maxAttempts:
            time.sleep(sleepTime)
            result = stbt.is_screen_black()
            counter += 1
        if counter > maxAttempts:
            return False
        return True

    def volumeUpSwitchDetection(self):
        try:
            stbt.wait_for_match("./images/t1/hds_max_volume_belt.png", region = stbt.Region(x=178, y=94, width=118, height=16))
        except stbt.MatchTimeout: 
            return False
        return True

    def volumeDownSwitchDetection(self):
        try:
            stbt.wait_for_match("./hds_part_volume_belt.png", region = stbt.Region(x=178, y=94, width=64, height=16))
        except stbt.MatchTimeout:
            return False
        else
            if stbt.match("./images/t1/hds_max_volume_belt.png", region = stbt.Region(x=178, y=94, width=118, height=16)):
                return False
            return True

    def lodeConfiguration(self, path):
        domeTree = minidom.parse(path)
        parameters = domeTree.firstChild # <parameters>
        paramChilds = parameters.childNodes

        soft = paramChilds[1] # <soft>
        softChilds = soft.getElementsByTagName("version")
        self.currentUpdateVersions.append(int(soft.childNodes[1].firstChild.data)) # <version>
        self.currentUpdateVersions.append(int(soft.childNodes[3].firstChild.data)) # <version>

        testChannels = paramChilds[7] # <test_channels>
        channels = testChannels.childNodes
        self.mainTestChannels.append(int(testChannels.childNodes[1].firstChild.data)) # <channel>
        self.mainTestChannels.append(int(testChannels.childNodes[3].firstChild.data)) # <channel>
        self.mainTestChannels.append(int(testChannels.childNodes[5].firstChild.data)) # <channel>
        self.mainTestChannels.append(int(testChannels.childNodes[7].firstChild.data)) # <channel>
        self.alternativeTestChannels.append(int(testChannels.childNodes[9].firstChild.data)) # <channel>
        self.alternativeTestChannels.append(int(testChannels.childNodes[11].firstChild.data)) # <channel>
        self.alternativeTestChannels.append(int(testChannels.childNodes[13].firstChild.data)) # <channel>
        self.alternativeTestChannels.append(int(testChannels.childNodes[15].firstChild.data)) # <channel>
        self.mainTerrestrialTestChannel = testChannels.childNodes[17].firstChild.data # <channel>
        self.alternativeTerrestrialTestChannel = testChannels.childNodes[19].firstChild.data # <channel>