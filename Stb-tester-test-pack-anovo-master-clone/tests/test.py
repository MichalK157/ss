import time
import stbt

class Test:
    timeBeforePress = 0.7 # czas pomiedzy wcisnieciami klawiszy pilota [s]
    maxPressesInMainMenu = 15 # maksymalna liczba przejsc w glownym Menu
    maxPressesInDiagnosticsMenu = 5 # maksymalna liczba przejsc w sekcji menu Ustawienia->Diagnostyka
    sleepTimeBeforeOCR = 2 # opoznienie przed OCR [s]
    sleepTimeAfterUSBCheck = 2 # opoznienie po sprawdzeniu USB [s]
    channelsTestingTime = 10 # czas testowania kanalu testowego [s]
    sleepTimeAfterDisplayCheck = 5 # opoznienie po sprawdzeniu wyswietlacza [s]
    afterChanelsConfirmedTime = 5 # czas po potwierdzeniu wyszukania kanalow [s]
    rebootWaitingTime = 300 # czas oczekiwania na wlaczenie po ustawieniach fabrycznych [s]
    searchingChanelsTime = 300 # czas oczekiwania na wyszukanie kanalow [s]
    currentUpdateVersions = [] # aktualne wersje oprogramowania
    mainTestChannels = [] # lista podstawowych kanalow testowych
    alternativeTestChannels = [] # lista alternatywnych kanalow testowych
    minSignalLevel = 0 # minimalna dopuszczalna sila sygnalu [%]
    minSignalQuality = 0 # minimalna dopuszczalna jakosc sygnalu [%]
    minWiFiSignalLevel = 0 # minimalna dopuszczalna sila sygnalu WiFi [%]
    timeBetwiFactorySettingsAndFunctionalTest = 10 # opoznienie przed rozpoczeciem testu funkcjonalnego po pierwszej instalacji
    SN = "" # numer serjny testowanego dekodera
    testsResults = {
        "power" : None,
        "messages" : None,
        "bills" : None,
        "rear_usb" : None,
        "side_usb" : None,
        "sn" : None,
        "soft_version" : None,
        "signal_level_1" : None,
        "signal_quality_1" : None,
        "signal_level_2" : None,
        "signal_quality_2" : None,
        "ethernet" : None,
        "wifi" : None,
        "card_reader" : None,
        "display" : None,
        "switches" : None,
        "hdd" : None,
        "timeshifting" : None,
        "terrestrial_siganl_level" : None,
        "terrestrial_siganl_quality" : None,
        "test_channels" : None,
        "smart_card" : None,
        "smart_card_number" : None,
        "mac" : None,
        "group" : None,
		"daiode" : None,
        "hds_autodiag_hardware_test" : None,
        "hds_factory_settings" : None,
        "max_index" : None
    }

    """ Procedura przeprowadajaca proces testowy zawierajacy czynnosci wkonywane podczaz wygrzewania wstepnego
        oraz przeprowadzenie testu funkcjonalnego dekodera
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.
            
        argumenty:
            - wyrzewanie - wlancza/wylancza czesc "wygraewanie wstapne" podczas testu, domyslna wartosc = True
            - testFunkc -  wlancza/wylancza czesc "test funkcjonalny" podczas testu, domyslan warosc = True """
    def start(self, wygrzewanie = True, testFunkc = True):
        if wygrzewanie:
            self.wygrzewanieWstepne()
            if testFunkc:
                time.sleep(timeBetwiFactorySettingsAndFunctionalTest)
        if testFunkc:
            self.testFunkcjonalny()

    """ Procedura preprowadzajaca proces wykonania ustawien fabrycznych oraz pierwszej intalacji 
        podczas wygrzewania wstepnego dekodera
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def wygrzewanieWstepne(self):
        self.ustawieniaFabryczne()
        self.pierwszaInstalacja()

    """ Procedura wirtualna przepowadzajaca proces testu funkjonalnego dekodera.
        Cialo procedury definiowane jest w klasach poszczegolnych modeli. """
    def testFunkcjonalny(self):
        pass

    """ Procedura wirtualna przepowadzajaca ustawienia fabryczne dekodera.
        Cialo procedury definiowane jest w klasach poszczegolnych modeli. """
    def ustawieniaFabryczne(self):
        pass

    """ Procedura wirtualna przepowadzajaca proces pierwszej instalacji dekodera.
        Cialo procedury definiowane jest w klasach poszczegolnych modeli. """
    def pierwszaInstalacja(self):
        pass

    """ Procedura przelanczajaca dekoder na zadany kanal
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.

        argumenty:
            - number - numer kanalu """
    def runChannel(number):
        keys = ["KEY_0", "KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5", "KEY_6", "KEY_7", "KEY_8", "KEY_9"]
        counter = 0
        num = str(number)
        length = len(num)
        while counter < length:
            key = num[counter : counter + 1]
            stbt.press(keys[int(key)], timeBeforePress)
            counter += 1

    """ Funkcja wciskajaca zadany przycisk dopoki nie odnajdzie szukanego tekstu w zadanym regionie
        argumenty:
            - text - wyszukiwany tekst
            - key - nazwa przycisku
            - region - obszar wyszukiwania, domyslna wartosc = stbt.Region.ALL
            - maxPresses - maksymalna liczba prob wcisniec przycisku i wyszukiwania tekstu, domyslna wartosc = maxPressesInMainMenu

        zwracane wartosci:
            - 0 - jesli proces wyszukiwania zakoncz sie sukcesem
            - -1 - w p.p. """
    def myPressUntilMatchText(text, key, region = stbt.Region.ALL, maxPresses = maxPressesInMainMenu):
        counter = 0
        time.sleep(sleepTimeBeforeOCR)
        result = stbt.match_text(text, None, region)
        while result.match == False and counter <= maxPresses:
            stbt.press(key, timeBeforePress)
            time.sleep(sleepTimeBeforeOCR)
            result = stbt.match_text(text, None, region)
            counter += 1
        if counter > maxPresses:
            return -1
        return 0

    """ Funkcja oczekujaca dopoki wyswietlany jest zadany tekst w zadanym regionie
        argumenty:
            - text - wyszukiwany tekst
            - region - obszar wyszukiwania, domyslna wartosc = stbt.Region.ALL
            - maxPresses - maksymalna liczba prob wyszukiwania tekstu, domyslna wartosc = 30
            - sleepTime - czas oczekiwania pomiedzy kolejnymi probami wyszukiwania tekstu [s], domyslna wartosc = 1
    
        zwracane wartosci:
            - True - jesli tekst w danym regionie zniknie przed maksymalna liczba prob
            - False - jesli tekst w danym regionie NIE zniknie przed maksymalna liczba prob """
    def myWaitWhileMatchText(text, region = stbt.Region.ALL, maxAttempts = 30, sleepTime = 1):
        counter = 0;
        result = stbt.match_text(text, None, region)
        while result.match == True and counter <= maxAttempts:
            time.sleep(sleepTime)
            counter += 1
            result = stbt.match_text(text, None, region)
        if counter > maxAttempts:
            return False
        return True

    """ Procedura tworzaca log z przeprowadzonego testu dekodera i zapisujaca wynik do pliku. """
    def makeLog():
        fileName = SN + "_" + str(time.localtime()) + ".log"
        file = open("./log/"+fileName, "w")
        
        if testsResults["messages"] == True:
            file.write("PASS. Brak wiadomosci.")
        elif testsResults["messages"] == False:
            file.write("FAIL. Wiadomosci nie usuniete.")
        if testsResults["bills"] == True:
            file.write("PASS. Brak rachunkow.")
        elif testsResults["bills"] == False:
            file.write("FAIL. Rachunki nie usuniete.")
        if testsResults["usb"] == True:
            file.write("PASS. Wykrto urzadzenie USB.")
        elif testsResults["usb"] == False:
            file.write("FAIL. Nie wykrto urzadzenia USB.")
        if testsResults["sn"] == True:
            file.write("PASS. SN zgodny z etykieta.")
        elif testsResults["sn"] == False:
            file.write("FAIL. SN nie zgodny z etykieta.")
        if testsResults["soft_version"] == True:
            file.write("PASS. Wersja oprogramowania prawidlowa.")
        elif testsResults["soft_version"] == False:
            file.write("FAIL. Wersja oprogramowania nieprawidlowa.")
        if testsResults["signal_level"] == True:
            file.write("PASS. Odpowiednia sila sygnalu.")
        elif testsResults["signal_level"] == False:
            file.write("FAIL. Nieodpowiednia sila sygnalu.")
        if testsResults["signal_quality"] == True:
            file.write("PASS. Odpowiednia jakosc sygnalu.")
        elif testsResults["signal_quality"] == False:
            file.write("FAIL. Nieodpowiednia jakosc sygnalu.")
        if testsResults["ethernet"] == True:
            file.write("PASS. Polaczenie kablowe prawidlowe.")
        elif testsResults["ethernet"] == False:
            file.write("FAIL. Polaczenie kablowe nieprawidlowe.")
        if testsResults["wifi"] == True:
            file.write("PASS. Polaczenie WiFi prawidlowe.")
        elif testsResults["wifi"] == False:
            file.write("FAIL. Polaczenie WiFi nieprawidlowe.")
        if testsResults["card_reader"] == True:
            file.write("PASS. Wykrto karte w czytniku.")
        elif testsResults["card_reader"] == False:
            file.write("FAIL. Nie wykrto karty w czytniku.")
        if testsResults["display"] == True:
            file.write("PASS. Wyswietlacz swieci prawidlowo.")
        elif testsResults["display"] == False:
            file.write("FAIL. Wyswietlacz swieci nieprawidlowo.")
        result = testsResults["swiches"]
        for switch in result.iterItems():
            if result[switch] == True:
                file.write("PASS. Wykryto wcisniecie klawisza '" + switch + "'.")
            elif result[switch] == False:
                file.write("FAIL. Nie Wykryto wcisniecia klawisza '" + switch + "'.")
        if testsResults["hdd"] == True:
            file.write("PASS. HDD dziala prawidowo.")
        elif testsResults["hdd"] == False:
            file.write("FAIL. HDD dziala nieprawidlowo.")
        if testsResults["terrestrial_siganl_level"] == True:
            file.write("PASS. Odpowiednia sila sygnalu naziemnego.")
        elif testsResults["terrestrial_siganl_level"] == False:
            file.write("FAIL. Nieodpowiednia sila sygnalu naziemnego.")
        if testsResults["terrestrial_siganl_quality"] == True:
            file.write("PASS. Odpowiednia jakosc sygnalu.")
        elif testsResults["terrestrial_siganl_quality"] == False:
            file.write("FAIL. Nieodpowiednia jakosc sygnalu naziemnego.")
        result = testsResults["test_channels"]
        for iterator in range(4):
            if result[iterator] == True:
                file.write("PASS. Kanal cwiartki nr " + iterator + "wyswietlany prawidlowo.")
            elif result[iterator] == False:
                file.write("FAIL. Kanal cwiartki nr " + iterator + "wyswietlany nie prawidlowo.")
        file.close()

    """ Procedura przeprowadzajaca proces testu pozczegolnych cwiartek synalu satelitarnego
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
    def testKanalow(self):
        result = []
        runChannel(self.mainTestChannels[3])
        time.sleep(self.channelsTestingTime)
        result.append(self.checkChannel(3))

        runChannel(self.mainTestChannels[2])
        time.sleep(self.channelsTestingTime)
        result.append(self.checkChannel(2))

        runChannel(self.mainTestChannels[1])
        time.sleep(self.channelsTestingTime)
        result.append(self.checkChannel(1))

        runChannel(self.mainTestChannels[0])
        time.sleep(self.channelsTestingTime)
        result.append(self.checkChannel(0))

        self.testsResults["test_channels"] = result

    """ Funkcja sprawdzajaca pojedyncza cwiartke sygnalu satelitarnego
        warunki poczatkowe:
            Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.

        argumenty:
            - number - numer cwiartki do sprawdzenia, numerowanie rozpoczyna sie od 0
            
        zwracane wartosci:
            - True - jesli testowany kanal glowny lub alternatywny wyswietlany jest poprawnie
            - False - w p.p. """
    def checkChannel(self, number):
        while True:
            print("Czy obraz jest wyswietalany prawidlowo?")
            print("1) Tak")
            print("2) Nie")
            input = int(input())
            if input == 1:
                return True
            elif input == 2:
                runChannel(self.alternativeTestsChannels[number])
                time.sleep(self.channelsTestingTime)
                print("Czy obraz jest wyswietalany prawidlowo?")
                print("1) Tak")
                print("2) Nie")
                input = input()
                if input == 1:
                    return True
                elif input ==2:
                    return False
                else:
                    print("Blad!!! Podaj liczbe 1 lub 2.")
            else:
                print("Blad!!! Podaj liczbe 1 lub 2.")