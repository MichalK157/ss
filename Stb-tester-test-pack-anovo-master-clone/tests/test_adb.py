from test import Test
import stbt
import time

class TestADB(Test):
    model = ""
    
    def __init__(self, model, configPath):
        self.model = model
        self.loadConfiguration(configPath)
    
        """ Procedura przeprowadzajaca proces testu funkcjonalnego dekodera
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def testFunkcjonalny(self, model):
        self.uruchomienieDekodera()
        self.ustawieniaFabryczne()
        self.pierwszaInstalacja()
        self.testCzytnikaKarty()
        time.sleep(20)
        self.wylaczKomunikatTVNaziemna()
        self.sprawdzUSB("rear_usb")
        
        if self.model == "3740SX":
            input = input("Usun Pendrive z tylnego gniazda USB i wloz Pendrive do gniazda bocznego.\n Potwierdz OK")
            while input != OK:
                input = input("Usun Pendrive z tylnego gniazda USB i wloz Pendrive do gniazda bocznego.\n Potwierdz OK")
            self.sprawdzUSB("side_usb")
        
        input = input("Podlacz sygnal 'Live' do slacza SAT")
        while input != "OK":
            input = input("Podlacz sygnal 'Live' do zlacza SAT")
            stbt.press("KEY_STAR", Test.timeBeforePress)
        stbt.press("KEY_3", Test.timeBeforePress)
        self.Test.testKanalow()
        stbt.press("KEY_SETUP", Test.timeBeforePress)
        
        if self.model == "3740SX" or self.model == "2050ST":
			self.TestADB.testTvNaziemnej()
		
        stbt.press("KEY_RIGHT", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        self.TestADB.sprawdzRachunki()
        stbt.press("KEY_BACK", Test.timeBeforePress)
        stbt.press("KEY_LEFT", Test.timeBeforePress)
        stbt.press("KEY_LEFT", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        self.TestADB.sprawdzWiadomosci()
        stbt.press("KEY_BACK", Test.timeBeforePress)
        stbt.press("KEY_LEFT", Test.timeBeforePress)
        stbt.press("KEY_LEFT", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        self.sprawdzSileIJakosSygnalu(1, stbt.Region(754, 223, width=56, height=30), stbt.Region(754, 263, width=56, height=30))
        if self.model == "3740SX":
            self.sprawdzSileIJakosSygnalu(2, stbt.Region(754, 400, width=56, height=30), stbt.Region(754, 445, width=56, height=30))
        stbt.press("KEY_BACK", Test.timeBeforePress)
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        self.TestADB.sprawdzSN()
        self.TestADB.testParowaniaKarty()
        self.TestADB.sprawdzMAC()
        self.TestADB.sprawdzGrupy()
        stbt.press("KEY_BACK", Test.timeBeforePress)
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        self.sprawdzWersjeOprogramowania()
        stbt.press("KEY_BACK", Time.timeBeforePress)
        self.myPressUntilMatchText("SIEC", "KEY_DOWN", stbt.Region(315, 380, width = 70, height =28))
        stbt.press("KEY_OK", Time.timeBeforePress)
        self.TestADB.sprawdzSiec()
        stbt.press("KEY_BACK", Test.timeBeforePress)
        stbt.press("KEY_BACK", Test.timeBeforePress)
		
        if self.model == "2850ST" or self.model == "2851S":
		    self.testDiody()

        if self.model == "3740SX":
            self.sprawdzWyswietlacz()
            self.sprawdzTimeshifting()
            self.sprawdzHDD()
		
	def testWygrzewanie(self):
		self.uruchomienieDekodera()
		#stbt.wait_for_match("obrazek po przejsciu aktywacji")
		self.ustawieniaFabryczne()
		stbt.mach_text("ANTENA TELEWIZJI NAZIEMNEJ", None, stbt.Region(410, 162, width = 460, height = 30))
		stbt.press("KEY_RIGHT", Test.timeBeforePress)
		stbt.press("KEY_OK", Test.timeBeforePress)
		stbt.press("KEY_SETUP", Test.timeBeforePress)
		stbt.press("KEY_RIGHT", Test.timeBeforePress)
		self.TestADB.sprawdzRachunki()
		stbt.press("KEY_BACK", Test.timeBeforePress)
		stbt.press("KEY_LEFT", Test.timeBeforePress)
		stbt.press("KEY_LEFT", Test.timeBeforePress)
		self.TestADB.sprawdzWiadomosci()
		stbt.press("KEY_BACK", Test.timeBeforePress)
		stbt.press("KEY_LEFT", Test.timeBeforePress)
		stbt.press("KEY_LEFT", Test.timeBeforePress)
		stbt.press("KEY_DOWN", Test.timeBeforePress)
		stbt.press("KEY_OK", Test.timeBeforePress)
		self.TestADB.testParowaniaKarty()
		stbt.press("KEY_BACK", Test.timeBeforePress)
		stbt.press("KEY_BACK", Test.timeBeforePress)

    def wylaczKomunikatTVNaziemna(self):
        try:
    		stbt.mach_text("ANTENA TELEWIZJI NAZIEMNEJ", None, stbt.Region(410, 162, width = 460, height = 30))
        except MatchTimeout:
            pass
        else:
            stbt.press("KEY_RIGHT", Test.timeBeforePress)
            stbt.press("KEY_OK", Test.timeBeforePress)

    """ Procedura sprawdzajaca czy w pamieci dekodera znajduja sie wiadomosci 
        warunki poczatkowe:
            Dekoder wyswietla ekran "Waidomosci" w sekcji "Menu->Wiadomosci" """
    def sprawdzWiadomosci(self):
        result = stbt.match_text("Nie", None, stbt.Region(149, 504, width=42, height=26))
        if  result.match == True:
            self.testResults["messages"] = True
        else:
            self.testResults["messages"] = False

    """ Procedura sprawdzajaca czy w pamieci dekodera znajduja sie informacjie o rachunkach 
        warunki poczatkowe:
            Dekoder wyswietla ekran "TV Rachunek" w sekcji "Menu->TV Rachunek" """
    def sprawdzRachunki(self):
        result = match_text("DO", None, stbt.Region(680, 150, width = 50, height = 30))
        if result == False:
            self.testsResults["bills"] = True
        else:
            self.testsResults["bills"] = False
    
    """ Procedura sprawdzajaca czy wykryto urzadzenie w gniezdzie USB dekodera
        warunki poczatkowe:
            Urzadzenie USB zostalo podlaczone do portu dekodera. """
    def sprawdzUSB(self, port):
        result = stbt.match_text("USB", None, stbt.Region(682, 162, width=70, height=28))
        if  result.match == True:
            stbt.press("KEY_RIGHT", Test.timeBeforePress)
            stbt.press("KEY_OK", Test.timeBeforePress)
            self.testsResults[port] = True
        else:
            self.testsResults[port] = False

    """ Procedura sprawdzajaca poprawnosc numeru seryjnego dekodera
        warunki poczatkowe:
            Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzSN(self, scannedSN):
        SN = stbt.ocr(None, stbt.Region(580, 205, width=245, height=28), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        print("Odczytany SN: ", SN)   
        if SN != scannedSN:
            self.testsResults["sn"] = False
        else:
            self.testsResults["sn"] = True

    """ Procedura sprawdzajaca poprawnosc adresu MAC dekodera
        warunki poczatkowe:
            Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzMAC(self, scannedMAC):
        MAC = stbt.ocr(None, stbt.Region(580, 406, width=207, height=28), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        print("Odczytany MAC: ", MAC)   
        if MAC != scannedMAC:
            self.testsResults["mac"] = False
        else:
            self.testsResults["mac"] = True

    def sprawdzGrupe(self):
        result = stbt.match_text("0", None, stbt.Region(580, 490, width=35, height=28))
        if  result == True:
            self.testResults["group"] = True
        else:
            self.testResults["group"] = False
    
    """ Prcedura sprawdzajaca wersje oprogramowania dekodera
        warunki poczatkowe:
            Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzWersjeOprogramowania(self):
        softVersion = stbt.ocr(None, stbt.Region(580, 327, width=70, height=28), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        if softVersion == currentUpdateVersions[0]:
            self.testsResults["soft_version"] = True
        else:
            self.testsResults["soft_version"] = False

    """ Procedura sprawdzajca sile oraz jakosc sygnalu satelitarnego
        warunki poczatkowe:
            Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzSileIJakosSygnalu(self, connector_number, level_region, quality_region):
        signalLevel = stbt.ocr(None, level_region, stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        sl = signalLevel[:-1]
        i = int(sl)
        print("Odczytana sila sygnalu: ", i)
        if i < self.minSignalLevel:
            self.testsResults["siganl_level_" + connector_number] = False
            return
        signalQuality = stbt.ocr(None, quality_region, stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        sq = signalQuality[:-1]
        j = int(sq)
        print("Odczytana jakosc sygnalu: ", j)
        if j < self.minSignalQuality:
            self.testsResults["signal_quality_" + connector_number] = False
            return
        self.testsResults["signal_level_" + connector_number] = True
        self.testsResults["singal_quality_" + connector_number] = True

    """ Procedura sprawdzajaca polaczenie sieciowe (kablowe i WiFi)
        warunki poczatkowe:
            Dekoder wyswietla ekran "Ustawienia sieci" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzSiec(self):
        ipTestResult = stbt.match_text("172.016", None, stbt.Region(580, 209, width=114, height=28))
        if  ipTestResult == False:
            self.testsResults["ethernet"] = False
        else:
            self.testsResults["ethernet"] = True

    """ Procedura wykonujaca sekwencje krokow robiaca ustawienia fabryczne
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def ustawieniaFabryczne(self):
        stbt.press("KEY_SETUP", Test.timeBeforePress)
        stbt.press("KEY_RED", Test.timeBeforePress)
        stbt.press("KEY_RED", Test.timeBeforePress)
        stbt.press("KEY_7", Test.timeBeforePress)
        stbt.press("KEY_3", Test.timeBeforePress)
        stbt.press("KEY_7", Test.timeBeforePress)
        stbt.press("KEY_3", Test.timeBeforePress)
        stbt.press("KEY_8", Test.timeBeforePress)

    """ Procedura wykonujaca sekwencje krokow przechodzaca proces pierwszej instalacji
        warunki poczatkowe:
            W dekoderze zosataly wlasnie zrobione ustawienia fabryczne lub dekoder wyswietla ekran "Pierwsza Instalacja". """
    def pierwszaInstalacja(self):
        try:
            stbt.wait_for_match("sciezka do obrazka lista kanalow", 60)
        except stbt.MatchTimeout:
            self.testsResults["power"] = False
            return
        self.testsResults["power"] = True
        try:
			stbt.wait_for_match("sciezka do obrazka aktualizacja oprogramowania", 60)
        except stbt.MatchTimeout:
            self.testsResults["signal_level_1"] = False
            self.testsResults["signal_quality_1"] = False
            return
        try:
            stbt.wait_for_match("sciezka do obrazka przycisku aktualizacja oprogramowania", 30, stbt.Region(260, 200, width = 690, height = 340 ))
        except stbt.MatchTimeout:
            try:
                stbt.wait_for_match("obrazek ptaszek(zaznaczenie - ethernet)", 20, stbt.Region(260, 200, width = 690, height = 340))
            except:
                stbt.press("KEY_UP", Test.timeBeforePress)
            stbt.press("KEY_OK", Test.timeBeforePress)
            stbt.press("KEY_OK", Test.timeBeforePress)
            try:
                stbt.wait_for_match("sciezka do obrazka odbierasz(aktywacja)", 30, stbt.Region(905, 450, width = 35, height = 30))
            except MatchTimeout:
                self.sprawdzSileIJakosSygnalu(1, stbt.Region(730, 365, width = 65, height = 25), stbt.Region(730, 405, width = 65, height = 25))
                if self.model == "3740SX":
                    self.sprawdzSileIJakosSygnalu(2, stbt.Region(730, 495, width = 65, height = 25), stbt.Region(730, 535, width = 65, height = 25))
                return
            try:
                stbt.wait_for_motion(30)
            except MotionTimeout:
                self.activationCode()
        else:
            stbt.press("KEY_OK", Test.timeBeforePress)
            self.uruchomienieDekodera()

    def uruchomienieDekodera():
        try:
            stbt.wait_for_match("sciezka do obrazka aktualizacja oprogramowania", 60)
        except stbt.MatchTimeout:
            self.testsResults["power"] = False
            return
        self.testsResults["power"] = True
        try:
            stbt.wait_for_match("sciezka do obrazka przycisku aktualizacja oprogramowania", 30, stbt.Region(260, 200, width = 690, height = 340 ))
        except stbt.MatchTimeout:
            try:
			    stbt.wait_for_match("sciezka do obrazka lista kanalow", 60)
            except stbt.MatchTimeout:
                self.testsResults["signal_level_1"] = False
                self.testsResults["signal_quality_1"] = False
                return
            try:
                stbt.wait_for_match("sciezka do obrazka odbierasz(aktywacja)", 30, stbt.Region(905, 450, width = 35, height = 30))
            except MatchTimeout:
                self.sprawdzSileIJakosSygnalu(1, stbt.Region(730, 365, width = 65, height = 25), stbt.Region(730, 405, width = 65, height = 25))
                if self.model == "3740SX":
                    self.sprawdzSileIJakosSygnalu(2, stbt.Region(730, 495, width = 65, height = 25), stbt.Region(730, 535, width = 65, height = 25))
                return
            try:
                stbt.wait_for_motion(30)
            except MotionTimeout:
                self.activationCode()
        else:
            stbt.press("KEY_OK", Test.timeBeforePress)
            self.uruchomienieDekodera()

    """ Procedura sprawdzajaca poprawnosc swiecenia poszczegolnych paneli wyswietlacza podczas gdy dekoder jest wlaczany i w stanie St-By
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def testWyswietlacza(self):
        pass

    """ Funkcja sprawdzajaca czy karta abonencka znajduje sie w czytniku kart 
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.

        zwracane wartosci:
            - True - jesli karta abonencka znajduje sie w czytniku
            - False - w p.p. """
    def testCzytnikaKarty(self):
        print("Wloz karte do czytnika.")
        self.testsResults["card_reader"] = myWaitWhileMatchText("BRAK KARTY", stbt.Region(509, 126, width = 239, height = 43))

    def testParowaniaKarty(self, scannedSmartCardNumber):
        smartCardNumber = stbt.ocr(None, stbt.Region(580, 205, width=245, height=28), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        print("Odczytany numer karty: ", smartCardNumber)   
        if smartCardNumber != scannedSmartCardNumber:
            self.testsResults["smart_card_number"] = False
        else:
            self.testsResults["smart_card_number"] = True

    def testTvNaziemnej(self):
        self.testsResults["terrestrial_siganl_level"] = []
        self.testsResults["terrestrial_siganl_quality"] = []
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_DOWN", Test.timeBeforePress)
        stbt.press("KEY_OK", Test.timeBeforePress)
        stbt.press("KEY_RIGHT", Test.timeBeforePress)
        channel_numbers = ["25", "55", "58"]
        for number in channel_numbers:
            Test.myPressUntilMatchText(number, "KEY_DOWN", stbt.Region(624, 399, width = 37, height = 26), 30)
            signalLevel = stbt.ocr(None, stbt.Region(514, 434, width=56, height=30), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
            sl = signalLevel[:-1]
            i = int(sl)
            print("Odczytana sila sygnalu: ", i)
            if i < self.minSignalLevel:
                self.testsResults["terrestrial_siganl_level"][channel_numbers.index(number)] = False
            else:
                self.testsResults["terrestrial_siganl_level"][channel_numbers.index(number)] = True
            signalQuality = stbt.ocr(None, stbt.Region(514, 601, width=56, height=30), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
            sq = signalQuality[:-1]
            j = int(sq)
            print("Odczytana jakosc sygnalu: ", j)
            if j < self.minSignalQuality:
                self.testsResults["terrestrial_siganl_quality"][channel_numbers.index(number)] = False
            else:
                self.testsResults["terrestrial_siganl_quality"][channel_numbers.index(number)] = True
        stbt.press("KEY_BACK", Test.timeBeforePress)
        stbt.press("KEY_BACK", Test.timeBeforePress)

    def activationCode(self):
        stbt.press("KEY_RED", Test.timeBeforePress)
        stbt.press("KEY_7", Test.timeBeforePress)
        stbt.press("KEY_2", Test.timeBeforePress)
        stbt.press("KEY_4", Test.timeBeforePress)
        stbt.press("KEY_7", Test.timeBeforePress)
        stbt.press("KEY_3", Test.timeBeforePress)
        stbt.press("KEY_3", Test.timeBeforePress)

    """ Procedura wczytujaca parametry testu z pliku konfiguracyjnego XML
        warunki poczatkowe:
            Plik konfiguracyjny zapisany jest w formacie XML oraz posiada z gory ustalona strukture.

        argumenty:
            - path - sciezka do pliku konfiguracyjnego """
    def loadConfiguration(self, path, model):
        domeTree = minidom.parse(path)
        parameters = domeTree.firstChild # <parameters>
        paramChilds = parameters.childNodes

        soft = paramChilds[1] # <soft>
        softChilds = soft.getElementsByTagName("version")
        for child in softChilds:
            if child.getAttribute("model") == model:
                self.currentUpdateVersions.append(int(child.data)) # <version>
    
        signal = paramChilds[3] # <signal>
        signalChilds = signal.childNodes
        self.minSignalLevel = int(signal.childNodes[1].firstChild.data) # <min_level>
        self.minSignalQuality = int(signal.childNodes[3].firstChild.data) # <min_quality>

        network = paramChilds[5] # <network>
        wifi = network.childNodes
        self.minWiFiSignalLevel = int(network.childNodes[1].firstChild.data) # <min_wifi_level>

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
    
        """print(currentUpdateVersions)
        print(minSignalLevel)
        print(minSignalQuality)
        print(minWiFiSignalLevel)
        print(mainTestChannels)
        print(alternativeTestChannels)"""