import stbt
import time
from xml.dom import minidom
import subprocess
import os
from test import Test


class TestDSIW74(Test):

    """ Konstruktor obiektow klasy TestDSIW74
        argumenty:
            - configPath - sciezka do pliku z parametrami testu dekodera"""
    def __init__(self, configPath):
        self.loadConfiguration(configPath)

    """ Procedura przeprowadzajaca proces testu funkcjonalnego dekodera
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def testFunkcjonalny(self):
        self.testCzytnikaKarty()
        self.sprawdzUSB()
        if testsResults["usb"]:
            stbt.press("KEY_BACK", self.timeBeforePress)
            time.sleep(self.sleepTimeAfterUSBCheck)
        wejdzWUstawienia()
        stbt.press("KEY_DOWN", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        time.sleep(self.sleepTimeBeforeOCR)
        self.sprawdzSN(input("Podaj SN dekodera: "))
        self.sprawdzWersjeOprogramowania()
        self.sprawdzSileIJakosSygnalu()
        stbt.press("KEY_BACK", self.timeBeforePress)
        stbt.press("KEY_DOWN", self.timeBeforePress)
        stbt.press("KEY_DOWN", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        time.sleep(self.sleepTimeBeforeOCR)
        self.sprawdzSiec()
        if testsResults["ethernet"]:
            stbt.press("KEY_BACK", self.timeBeforePress)
            stbt.press("KEY_BACK", self.timeBeforePress)
        stbt.press("KEY_BACK", self.timeBeforePress)
        stbt.press("KEY_BACK", self.timeBeforePress)
        stbt.press("KEY_LEFT", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        sprawdzWiadomosci()
        stbt.press("KEY_BACK", self.timeBeforePress)
        myPressUntilMatchText("TV RACHUNEK", "KEY_RIGHT", stbt.Region(515, 599, width=242, height=54))
        stbt.press("KEY_OK", self.timeBeforePress)
        self.sprawdzRachunki()
        stbt.press("KEY_BACK", self.timeBeforePress)
        stbt.press("KEY_BACK", self.timeBeforePress)
        self.testWyswietlacza()
        time.sleep(sleepTimeAfterDisplayCheck)
        self.testKanalow()
        self.testKlawiszy()

    """ Procedura sprawdzajaca czy w pamieci dekodera znajduja sie wiadomosci 
        warunki poczatkowe:
            Dekoder wyswietla ekran "Waidomosci" w sekcji "Menu->Wiadomosci" """
    def sprawdzWiadomosci():
        result = stbt.wait_for_match("images/t1/no_message_image.png")
        if result.match == False:
            self.testsResults["messages"] = False
        else:
            self.testsResults["messages"] = True

    """ Procedura sprawdzajaca czy w pamieci dekodera znajduja sie informacjie o rachunkach 
        warunki poczatkowe:
            Dekoder wyswietla ekran "TV Rachunek" w sekcji "Menu->TV Rachunek" """
    def sprawdzRachunki(self):
        result = stbt.wait_for_match("images/t1/no_bill_image.png")
        if result.match == False:
            self.testsResults["bills"] = False
        else:
            self.testsResults["bills"] = True
    
    """ Procedura sprawdzajaca czy wykryto urzadzenie w gniezdzie USB dekodera
        warunki poczatkowe:
            Urzadzenie USB zostalo podlaczone do portu dekodera. """
    def sprawdzUSB(self):
        result = stbt.match_text("USB", None, stbt.Region(696, 121, width=90, height=54))
        if result.match == False:
            self.testsResults["usb"] = False
        else:
            self.testsResults["usb"] = True

    """ Procedura wchodzaca w sekcje "Ustawenia" w menu glowym 
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def wejdzWUstawienia(self):
        stbt.press("KEY_MENU", self.timeBeforePress)
        myPressUntilMatchText("USTAWIENIA", "KEY_RIGHT", stbt.Region(542, 611, width=188, height=32))
        stbt.press("KEY_OK", self.timeBeforePress)

    """ Procedura sprawdzajaca poprawnosc numeru seryjnego dekodera
        warunki poczatkowe:
            Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzSN(self, scannedSN):
        SN = stbt.ocr(None, stbt.Region(698, 202, width=234, height=28), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        print("Odczytany SN: ", SN)   
        if SN != scannedSN:
            self.testsResults["sn"] = False
        else:
            self.testsResults["sn"] = True

    """ Prcedura sprawdzajaca wersje oprogramowania dekodera
        warunki poczatkowe:
            Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzWersjeOprogramowania(self):
        updateVersion = stbt.ocr(None, stbt.Region(706, 296, width=65, height=27), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        uv = int(updateVersion)
        print("Odczytana wersja oprogramowania: ", uv)
        if uv != self.currentUpdateVersions[0] and uv != self.currentUpdateVersions[1]:
            self.testsResults["soft_version"] = False
        else:
            self.testsResults["soft_version"] = True

    """ Procedura sprawdzajca sile oraz jakosc sygnalu satelitarnego
        warunki poczatkowe:
            Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzSileIJakosSygnalu(self):
        signalLevel = stbt.ocr(None, stbt.Region(1119, 436, width=53, height=36), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        sl = signalLevel[:-1]
        i = int(sl)
        print("Odczytana sila sygnalu: ", i)
        if i < self.minSignalLevel:
            self.testsResults["siganl_level"] = False
            return
        signalQuality = stbt.ocr(None, stbt.Region(1116, 488, width=54, height=28), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        sq = signalQuality[:-1]
        j = int(sq)
        print("Odczytana jakosc sygnalu: ", j)
        if j < self.minSignalQuality:
            self.testsResults["signal_quality"] = False
            return
        self.testsResults["signal_level"] = True
        self.testsResults["singal_quality"] = True

    """ Procedura sprawdzajaca polaczenie sieciowe (kablowe i WiFi)
        warunki poczatkowe:
            Dekoder wyswietla ekran "Ustawienia sieci" w sekcji "Menu->Ustawienia->Diagnostyka" """
    def sprawdzSiec(self):
        ipTestResult = stbt.match_text("172.16", None, stbt.Region(707, 297, width=66, height=27))
        if  ipTestResult == False:
            self.testsResults["ethernet"] = False
            return
        stbt.press("KEY_INFO", self.timeBeforePress)
        stbt.press("KEY_DOWN", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        time.sleep(self.sleepTimeBeforeOCR)
        wifiLevel = stbt.ocr(None, stbt.Region(1110, 281, width=58, height=35), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
        wl = wifiLevel[:-1]
        i = int(wl)
        print("Odczytana sila sygnalu WiFi: ", i)
        if  i < self.minWiFiSignalLevel:
            self.testsResults["wifi"] = False
            return
        self.testsResults["ethernet"] = True
        self.testsResults["wifi"] = True

    """ Procedura wykonujaca sekwencje krokow robiaca ustawienia fabryczne
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def ustawieniaFabryczne(self):
        wejdzWUstawienia()
        myPressUntilMatchText("FABRYCZNE", "KEY_DOWN", stbt.Region(507, 339, width=182, height=36), self.maxPressesInDiagnosticsMenu) # sztuczka polegajaca na tym, ze slowo "FABRYCZNE" zmienia swoja pozcje na ekranie gdy opcja "USTAWIENIA FABRYCZNE" jest zaznaczona
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_1", self.timeBeforePress)
        stbt.press("KEY_2", self.timeBeforePress)
        stbt.press("KEY_5", self.timeBeforePress)
        stbt.press("KEY_7", self.timeBeforePress)
        stbt.press("KEY_INFO", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)

    """ Procedura wykonujaca sekwencje krokow przechodzaca proces pierwszej instalacji
        warunki poczatkowe:
            W dekoderze zosataly wlasnie zrobione ustawienia fabryczne lub dekoder wyswietla ekran "Pierwsza Instalacja". """
    def pierwszaInstalacja(self):
        stbt.wait_for_match("images/t1/first_installation_image.png", self.rebootWaitingTime)
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.wait_for_match("images/t1/searching_chanels_done_image.png", self.searchingChanelsTime)
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_BACK", self.afterChanelsConfirmedTime)
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)
        stbt.press("KEY_OK", self.timeBeforePress)

    """ Procedura sprawdzajaca dzialanie klawiszy na panelu przednim dekodera
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. 
        
            argumenty:
                - maxAttempts - maksyalna liczba prob detekcji wcisniecia klawisza, domyslna wartosc = 5. """
    def testKlawiszy(self, maxAttempts = 5):
        result = {}
        counter = 0

        print("Wcisnij klawisz 'P-'")
        detection = channelSwitchDetection(self.mainTestChannels[0])
        while detection[0] != 1 and counter < maxAttempts:
            detection = channelSwitchDetection(self.mainTestChannels[0])
            counter += 1
        if counter == maxAttempts:
            result["P-"] = False
        else:
            result["P-"] = True
        
        print("Wcisnij klawisz 'P+'")
        time.sleep(5)
        counter = 0
        detection = channelSwitchDetection(detection[1])
        while detection[0] != 2 and counter < maxAttempts:
            detection = channelSwitchDetection(detection[1])
            counter += 1
        if counter == maxAttempts:
            result["P+"] = False
        else:
            result["P+"] = True

        print("Wcisnij klawisz 'St-By'")
        time.sleep(5)
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

    """ Procedura sprawdzajaca poprawnosc swiecenia poszczegolnych paneli wyswietlacza podczas gdy dekoder jest wlaczany i w stanie St-By
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def testWyswietlacza(self):
        stbt.press("KEY_8", self.timeBeforePress)
        stbt.press("KEY_8", self.timeBeforePress)
        stbt.press("KEY_8", self.timeBeforePress)
        time.sleep(5)
        print("Czy wyswietalcz dziala prawidlowo?")
        print("1) Tak")
        print("2) Nie")
        result = input()
        r = int(result)
        if r == 2:
            self.testsResults["display"] = False
            return
        stbt.press("KEY_POWER", self.timeBeforePress)
        print("Czy na wyswietalczu pojawil sie zegar i swieci prawidlowo(przyciemniony)?")
        print("1) Tak")
        print("2) Nie")
        result = input()
        r = int(result)
        if r == 2:
            self.testsResults["display"] = False
            return
        time.sleep(10)
        stbt.press("KEY_POWER", self.timeBeforePress)
        self.testsResults["display"] = True

    """ Funkcja sprawdzajaca czy klawisz "P-" lub "P+" na panelu glownym dekodera zosatl wcisniety
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.

        argumenty:
            - channelToCompare - numer kanalu aktalnie odbieranego przez dekoder
        
        zwracane wartosci:
            tablica zawierajaca w pierwszej komorce watosci
                - 1 - jesli wykryto wicisniecie klawisza "P-"
                - 2 - jesli wykryto wicisniecie klawisza "P+"
                - -1 - jesli NIE wykryto wcisniecia klawisza "P-" lub "P+"
            oraz w drugiej komorce numer kanalu odbieranego po przelaczeniu """
    def channelSwitchDetection(channelToCompare):
        result = [0, 0]
        try:
            stbt.wait_for_match("images/t1/up_arrow_image.png") # oczekiwanie na wcisnienie przycisku
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

    """ Funkcja sprawdzajaca czy klawisz "St-By" na panelu glownym dekodera zosatl wcisniety
        argumenty:
            - maxAttempts - maksymalna liczba prob, domyslna wartosc = 10
            - sleepTime - czas oczekiwania pomiedzy kolejnymi probami [s], domyslna wartosc = 1
        
        zwracane wartosci:
            - True - jesli wicisniecie klawisza "St-By" zostanie wykryte
            - False - w p.p. """
    def stbySwitchDetection(maxAttempts = 10, sleepTime = 1):
        counter = 0
        result = stbt.is_screen_black()
        while result.black == False and counter <= maxAttempts:
            time.sleep(sleepTime)
            result = stbt.is_screen_black()
            counter += 1
        if counter > maxAttempts:
            return False
        return True

    """ Funkcja sprawdzajaca czy karta abonencka znajduje sie w czytniku kart 
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.

        zwracane wartosci:
            - True - jesli karta abonencka znajduje sie w czytniku
            - False - w p.p. """
    def testCzytnikaKarty(self):
        print("Wloz karte do czytnika.")
        self.testsResults["card_reader"] = myWaitWhileMatchText("BRAK KARTY", stbt.Region(509, 126, width = 239, height = 43))

    """ Procedura wczytujaca parametry testu z pliku konfiguracyjnego XML
        warunki poczatkowe:
            Plik konfiguracyjny zapisany jest w formacie XML oraz posiada z gory ustalona strukture.

        argumenty:
            - path - sciezka do pliku konfiguracyjnego """
    def loadConfiguration(self, path):
        domTree = minidom.parse(path)
        parameters = domTree.firstChild # <parameters>
        paramChilds = parameters.childNodes
    
        soft = paramChilds[1] # <soft>
        self.currentUpdateVersions.append(int(soft.childNodes[1].firstChild.data)) # <version>
        self.currentUpdateVersions.append(int(soft.childNodes[3].firstChild.data)) # <version>
    
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
