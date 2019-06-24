import stbt
import time
from xml.dom import minidom
import subprocess
import os
from test_dsi_w74 import TestDSIW74
from test_adb_3740sx import TestADB3740SX 

timeBeforePress = 0.7 # czas pomiedzy wcisnieciami klawiszy pilota [s]
maxPressesInMainMenu = 15 # maksymalna liczba przejsc w glownym Menu
maxPressesInDiagnosticsMenu = 5 # maksymalna liczba przejsc w sekcji menu Ustawienia->Diagnostyka
sleepTimeBeforeOCR = 2 # opoznienie przed OCR [s]
sleepTimeAfterUSBCheck = 2 # opoznienie po sprawdzeniu USB [s]
afterChanelsConfirmedTime = 5 # czas po potwierdzeniu wyszukania kanalow [s]
rebootWaitingTime = 300 # czas oczekiwania na wlaczenie po ustawieniach fabrycznych [s]
searchingChanelsTime = 300 # czas oczekiwania na wyszukanie kanalow [s]
currentUpdateVersions = list() # aktualne wersje oprogramowania
mainTestChannels = list() # lista podstawowych kanalow testowych
alternativeTestChannels = list() # lista alternatywnych kanalow testowych
minSignalLevel = 0 # minimalna dopuszczalna sila sygnalu [%]
minSignalQuality = 0 # minimalna dopuszczalna jakosc sygnalu [%]
minWiFiSignalLevel = 0 # minimalna dopuszczalna sila sygnalu WiFi [%]
averageAudioRMSVolume8 = 0.0875325530273874 # srednia RMS pomiaru audio (Player) przy glosnosci rownej 8 (50%)
rmsStandardDeviationVolume8 = 0.00290717260451407 # srednie odchylenie standardowe RMS pomiaru audio (Player) przy glosnosci rownej 8 (50%)
averageAudioRMSVolume16 = 0.395551387190217 # srednia RMS pomiaru audio (Player) przy glosnosci rownej 16 (100%)
rmsStandardDeviationVolume16 = 0.00371410933968001 # srednie odchylenie standardowe RMS pomiaru audio (Player) przy glosnosci rownej 16 (100%)
rmsLatitudeCoefficient = 0.05 # wspolcynnik tolerancji dla RMS pomiaru audio
timeBetwiFactorySettingsAndFunctionalTest = 10 # opoznienie przed rozpoczeciem testu funkcjonalnego po pierwszej instalacji

""" Procedura preprowadzajaca proces wykonania ustawien fabrycznych oraz pierwszej intalacji 
    podczas wygrzewania wstepnego dekodera
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
def test_wygrzewanieWstepneDsiW74():
    ustawieniaFabryczne()
    pierwszaInstalacja()

""" Procedura przeprowadajaca proces testowy zawierajacy wykonanie ustawien fabrycznych i pierwszej instalacji
    oraz przeprowadzenie testu funkcjonalnego dekodera
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
def test_testDSI():
    test_wygrzewanieWstepneDsiW74()
    time.sleep(timeBetwiFactorySettingsAndFunctionalTest)
    test_funkcjonalnyDsiW74()

""" Procedura przeprowadzajaca proces testu funkcjonalnego dekodera
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. 
        
    zwracane wartosci:
        Wyniki poszczegolnych czesci testu zzwracane sa na standardowe wyjscie."""
def test_funkcjonalnyDsiW74():
    loadConfiguration("/var/lib/stbt/test-pack/tests/test_config.xml")

    # tutaj pownien byc komunikat proszacy uzytkownika o wlozenie karty do czytnika
    result = testCzytnikaKarty()
    if result == 0:
        print("PASS. Wykrto karte w czytniku.")
    else:
        print("FAIL. Nie wykrto karty w czytniku.")
        #return
    result = sprawdzUSB()
    if result == 0:
        print("PASS. Wykrto urzadzenie USB.")
        stbt.press("KEY_BACK", timeBeforePress)
        time.sleep(sleepTimeAfterUSBCheck)
    else:
        print("FAIL. Nie wykrto urzadzenia USB.")
        #return
    wejdzWUstawienia()
    stbt.press("KEY_DOWN", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)
    time.sleep(sleepTimeBeforeOCR)
    result = sprawdzSN("ESCA015123282341E")     # tutaj musi byc jakis input SN
    if result == 0:
        print("PASS. SN zgodny z etykieta.")
    else:
        print("FAIL. SN nie zgodny z etykieta.")
        #return
    result = sprawdzWersjeOprogramowania()
    if result == 0:
        print("PASS. Wersja oprogramowania prawidlowa.")
    else:
        print("FAIL. Wersja oprogramowania nieprawidlowa.")
        #return
    result = sprawdzSileIJakosSygnalu()
    if result == 0:
        print("PASS. Odpowiednia sila sygnalu.")
        print("PASS. Odpowiednia jakosc sygnalu.")
    elif result == -1:
        print("FAIL. Nieodpowiednia sila sygnalu.")
        #return
    else:
        print("PASS. Odpowiednia sila sygnalu.")
        print("FAIL. Nieodpowiednia jakosc sygnalu.")
        raise
        #return
    stbt.press("KEY_BACK", timeBeforePress)
    stbt.press("KEY_DOWN", timeBeforePress)
    stbt.press("KEY_DOWN", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)
    time.sleep(sleepTimeBeforeOCR)
    result = sprawdzSiec()
    if result == 0:
        print("PASS. Polaczenie kablowe prawidlowe.")
        print("PASS. Polaczenie WiFi prawidlowe.")
        stbt.press("KEY_BACK", timeBeforePress)
        stbt.press("KEY_BACK", timeBeforePress)
    elif result == -1:
        print("FAIL. Polaczenie kablowe nieprawidlowe.")
        #return
    else:
        print("PASS. Polaczenie kablowe prawidlowe.")
        print("FAIL. Polaczenie WiFi nieprawidlowe.")
        stbt.press("KEY_BACK", timeBeforePress)
        stbt.press("KEY_BACK", timeBeforePress)
        #return
    stbt.press("KEY_BACK", timeBeforePress)
    stbt.press("KEY_BACK", timeBeforePress)
    stbt.press("KEY_LEFT", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)
    result = sprawdzWiadomosci()
    if result == 0:
        print("PASS. Brak wiadomosci.")
        stbt.press("KEY_BACK", timeBeforePress)
    else:
        print("FAIL. Wiadomosci nie usuniete.")
        stbt.press("KEY_BACK", timeBeforePress)
        #return
    myPressUntilMatchText("TV RACHUNEK", "KEY_RIGHT", stbt.Region(515, 599, width=242, height=54))
    stbt.press("KEY_OK", timeBeforePress)
    result = sprawdzRachunki()
    if result == 0:
        print("PASS. Brak rachunkow.")
        stbt.press("KEY_BACK", timeBeforePress)
        stbt.press("KEY_BACK", timeBeforePress)
    else:
        print("FAIL. Rachunki nie usuniete.")
        stbt.press("KEY_BACK", timeBeforePress)
        stbt.press("KEY_BACK", timeBeforePress)
        #return
    result = testWyswietlacza()
    if result == 0:
        print("PASS. Wyswietlacz swieci prawidlowo.")
    elif result == -1:
        print("FAIL. Wyswietlacz swieci nieprawidlowo gdy dekoder jest wlaczany.")
        #return
    else:
        print("FAIL. Wyswietlacz swieci nieprawidlowo gdy dekoder jest w trybie St-By.")
        #return

    time.sleep(5)

    testKanalow()

    time.sleep(5)

    result = testKlawiszy()
    if result[0] == 0:
        print("PASS. Wykryto wcisniecie klawisza 'P-'.")
    else:
        print("FAIL. Nie Wykryto wcisniecia klawisza 'P-'.")
    if result[1] == 0:
        print("PASS. Wykryto wcisniecie klawisza 'P+'.")
    else:
        print("FAIL. Nie Wykryto wcisniecia klawisza 'P+'.")
    if result[2] == 0:
        print("PASS. Wykryto wcisniecie klawisza 'St-By'.")
    else:
        print("FAIL. Nie Wykryto wcisniecia klawisza 'St-By'.")

# sprawdzenie 4 kanalow testowych
def testKanalow():
    #sprawdzanie kanalow
    runChannel(mainTestChannels[3])
    time.sleep(10)
    #tutaj musi byc jakies sprawdzenie obrazu
    runChannel(mainTestChannels[2])
    time.sleep(10)
    #tutaj musi byc jakies sprawdzenie obrazu
    runChannel(mainTestChannels[1])
    time.sleep(10)
    #tutaj musi byc jakies sprawdzenie obrazu
    runChannel(mainTestChannels[0])
    time.sleep(10)
    #tutaj musi byc jakies sprawdzenie obrazu

""" Funkcja sprawdzajaca dzialanie klawiszy na panelu przednim dekodera
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. 
        
        argumenty:
            - maxAttempts - maksyalna liczba prob detekcji wcisniecia klawisza
            
        zwracane wartosci:
            - result - tablica trojelementowa zawierajaca warosci
                - 0 jesli wykryto wcisiniecie klawisza
                - -1 w p.p.
            w komorce o indeksie
                - 0 dla klawisza "P-" 
                - 1 dla klawisza "P+" 
                - 2 dla klawisza "St-By" """
def testKlawiszy(maxAttempts = 5):
    result = []
    counter = 0
    
    
    # tutaj musi byc komunikat do uzytkownika "wcisnij klawisz 'P-'"
    detection = channelSwitchDetection(mainTestChannels[0])
    while detection[0] != 1 and counter < maxAttempts:
        detection = channelSwitchDetection(mainTestChannels[0])
        counter += 1
    if counter == maxAttempts:
        result.append(-1)
    else:
        result.append(0)

    # tutaj musi byc komunikat do uzytkownika "wcisnij klawisz 'P+'"
    time.sleep(5)
    counter = 0
    detection = channelSwitchDetection(detection[1])
    while detection[0] != 2 and counter < maxAttempts:
        detection = channelSwitchDetection(detection[1])
        counter += 1
    if counter == maxAttempts:
        result.append(-1)
    else:
        result.append(0)

    # tutaj musi byc komunikat do uzytkownika "wcisnij klawisz 'St-By'"
    time.sleep(5)
    counter = 0
    detection = stbySwitchDetection()
    while detection == -1 and counter < maxAttempts:
        detection = stbySwitchDetection()
        counter += 1
    if counter == maxAttempts:
        result.append(-1)
    else:
        result.append(0)

    return result

""" Funkcja sprawdzajaca czy klawisz "P-" lub "P+" na panelu glownym dekodera zosatl wcisniety
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.

    argumenty:
        - channelToCompare - numer kanalu aktalnie odbieranego przez dekoder
        - maxAttempts - maksymalna liczba prob, domyslna wartosc = 10
        
    zwracane wartosci:
        tablica zawierajaca w pierwszej komorce watosci
            - 1 - jesli wykryto wicisniecie klawisza "P-"
            - 2 - jesli wykryto wicisniecie klawisza "P+"
            - -1 - jesli NIE wykryto wcisniecia klawisza "P-" lub "P+"
        oraz w drugiej komorce numer kanalu odbieranego po przelaczeniu """
def channelSwitchDetection(channelToCompare, maxAttempts = 10):
    result = [0, 0]
    stbt.wait_for_match("images/t1/up_arrow_image.png") # oczekiwanie na wcisnienie przycisku
    channelNumber = stbt.ocr(None, stbt.Region(90, 592, width=45, height=41), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
    cn = int(channelNumber)
    result[1] = cn
    if cn < channelToCompare:
        result[0] = 1
    elif cn > channelToCompare:
        result[0] = 2
    else:
        result[0] = -1
    return result

""" Funkcja sprawdzajaca czy klawisz "St-By" na panelu glownym dekodera zosatl wcisniety
    argumenty:
        - maxAttempts - maksymalna liczba prob, domyslna wartosc = 10
        - sleepTime - czas oczekiwania pomiedzy kolejnymi probami [s], domyslna wartosc = 1
        
    zwracane wartosci:
        - 0 - jesli wicisniecie klawisza "St-By" zostanie wykryte
        - -1 - w p.p. """
def stbySwitchDetection(maxAttempts = 10, sleepTime = 1):
    counter = 0
    result = stbt.is_screen_black()
    while result.black == False and counter <= maxAttempts:
        time.sleep(sleepTime)
        result = stbt.is_screen_black()
        counter += 1
    if counter > maxAttempts:
        return -1
    return 0

""" Funkcja sprawdzajaca poprawnosc swiecenia poszczegolnych paneli wyswietlacza podczas gdy dekoder jest wlaczany i w stanie St-By
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.
        
    zwracane wartosci:
        - 0 - jesli wyswietlacz swieci poprawnie
        - -1 - jesli wyswietlacz nie swieci prawidlowo podczas gdy dekoder jest wlaczany
        - -2 - jesli wyswietlacz nie swieci prawidlowo podczas gdy dekoder jest w stanie St-By """
def testWyswietlacza():
    stbt.press("KEY_8", timeBeforePress)
    stbt.press("KEY_8", timeBeforePress)
    stbt.press("KEY_8", timeBeforePress)
    time.sleep(5)
    result = True # tutaj powinno byc pytanie do uzytkownika czy wyswietalcz swieci prawidlowo
    if result == False:
        return -1
    stbt.press("KEY_POWER", timeBeforePress)
    result = True # tutaj powinno byc pytanie do uzytkownika czy na wyswietalczu pojawia sie zegar i swieci prawidlowo(przyciemniony)
    if result == False:
        return -2
    time.sleep(10)
    stbt.press("KEY_POWER", timeBeforePress)
    return 0

""" Funkcja sprawdzajaca czy karta abonencka znajduje sie w czytniku kart 
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane.

    zwracane wartosci:
        - 0 - jesli karta abonencka znajduje sie w czytniku
        - -1 - w p.p. """
def testCzytnikaKarty():
    return myWaitWhileMatchText("BRAK KARTY", stbt.Region(509, 126, width = 239, height = 43))

""" Funkcja sprawdzajaca czy w pamieci dekodera znajduja sie wiadomosci 
    warunki poczatkowe:
        Dekoder wyswietla ekran "Waidomosci" w sekcji "Menu->Wiadomosci"

    zwracane wartosci:
        - 0 - jesli w pamieci dekodera NIE znajduja sie zadne widomosci
        - -1 - w p.p. """
def sprawdzWiadomosci():
    result = stbt.wait_for_match("images/t1/no_message_image.png")
    if result.match == False:
        return -1
    return 0

""" Funkcja sprawdzajaca czy w pamieci dekodera znajduja sie informacjie o rachunkach 
    warunki poczatkowe:
        Dekoder wyswietla ekran "TV Rachunek" w sekcji "Menu->TV Rachunek"

    zwracane wartosci:
        - 0 - jesli w pamieci dekodera NIE znajduja sie zadne informacje o rachunkach
        - -1 - w p.p. """
def sprawdzRachunki():
    result = stbt.wait_for_match("images/t1/no_bill_image.png")
    if result.match == False:
        return -1
    return 0
    
""" Funkcja sprawdzajaca czy wykryto urzadzenie w gniezdzie USB dekodera
    warunki poczatkowe:
        Urzadzenie USB zostalo podlaczone do portu dekodera.

    zwracane wartosci:
        - 0 - jesli wykryto komunikat dekodera o wykryciu urzadzenia USB
        - -1 - w p.p. """
def sprawdzUSB():
    result = stbt.match_text("USB", None, stbt.Region(696, 121, width=90, height=54))
    if result.match == False:
        return -1
    return 0

""" Procedura wchodzaca w sekcje "Ustawenia" w menu glowym 
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
def wejdzWUstawienia():
    stbt.press("KEY_MENU", timeBeforePress)
    myPressUntilMatchText("USTAWIENIA", "KEY_RIGHT", stbt.Region(542, 611, width=188, height=32))
    stbt.press("KEY_OK", timeBeforePress)

""" Funkcja sprawdzajaca poprawnosc numeru seryjnego dekodera
    warunki poczatkowe:
        Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka"

    zwracane wartosci:
        - 0 - jesli SN w pamieci dekodera zgodny z SN zeskanowanym z etykiety
        - -1 - w p.p. """
def sprawdzSN(scannedSN):
    SN = stbt.ocr(None, stbt.Region(698, 202, width=234, height=28), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
    print("Odczytany SN: ", SN)   
    if SN != scannedSN:
        return -1
    return 0

""" Funkcja sprawdzajaca wersje oprogramowania dekodera
    warunki poczatkowe:
        Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka"

    zwracane wartosci:
        - 0 - jesli oprogramowanie jest aktualne
        - -1 - w p.p. """
def sprawdzWersjeOprogramowania():
    updateVersion = stbt.ocr(None, stbt.Region(706, 296, width=65, height=27), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
    uv = int(updateVersion)
    print("Odczytana wersja oprogramowania: ", uv)
    if uv != currentUpdateVersions[0] and uv != currentUpdateVersions[1]:
        return -1
    return 0

""" Funkcja sprawdzajca sile oraz jakosc sygnalu satelitarnego
    warunki poczatkowe:
        Dekoder wyswietla ekran "Infrmacje techniczne" w sekcji "Menu->Ustawienia->Diagnostyka"

    zwracane wartosci:
        - 0 - jesli test przebiegnie pomyslnie
        - -1 - niewystarczajaca sila sygnalu satelitarnego
        - -2 - niewystarczajaca sila sygnalu satelitarnego  """
def sprawdzSileIJakosSygnalu():
    signalLevel = stbt.ocr(None, stbt.Region(1119, 436, width=53, height=36), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
    sl = signalLevel[:-1]
    i = int(sl)
    print("Odczytana sila sygnalu: ", i)
    if i < minSignalLevel:
        return -1
    signalQuality = stbt.ocr(None, stbt.Region(1116, 488, width=54, height=28), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
    sq = signalQuality[:-1]
    j = int(sq)
    print("Odczytana jakosc sygnalu: ", j)
    if j < minSignalQuality:
        return -2
    return 0

""" Funkcja sprawdzajaca polaczenie sieciowe (kablowe i WiFi)
    warunki poczatkowe:
        Dekoder wyswietla ekran "Ustawienia sieci" w sekcji "Menu->Ustawienia->Diagnostyka"

    zwracane wartosci:
        - 0 - jesli test przebiegnie pomyslnie
        - -1 - blad polaczenia kalowego, UWAGA: polaczenie WiFi nie bedzie sprawdzane
        - -2 - blad polaczenia WiFi """
def sprawdzSiec():
    ipTestResult = stbt.match_text("172.16", None, stbt.Region(707, 297, width=66, height=27))
    if  ipTestResult == False:
        return -1
    stbt.press("KEY_INFO", timeBeforePress)
    stbt.press("KEY_DOWN", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)
    time.sleep(sleepTimeBeforeOCR)
    wifiLevel = stbt.ocr(None, stbt.Region(1110, 281, width=58, height=35), stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD)
    wl = wifiLevel[:-1]
    i = int(wl)
    print("Odczytana sila sygnalu WiFi: ", i)
    if  i < minWiFiSignalLevel:
        return -2
    return 0

""" Procedura wykonujaca sekwencje krokow robiaca ustawienia fabryczne
    warunki poczatkowe:
        Dekoder jest w stanie wyswietlania tresci obrazu, wszystkie menu sa wylaczane. """
def ustawieniaFabryczne():
    wejdzWUstawienia()
    myPressUntilMatchText("FABRYCZNE", "KEY_DOWN", stbt.Region(507, 339, width=182, height=36), maxPressesInDiagnosticsMenu) # sztuczka polegajaca na tym, ze slowo "FABRYCZNE" zmienia swoja pozcje na ekranie gdy opcja "USTAWIENIA FABRYCZNE" jest zaznaczona
    stbt.press("KEY_OK", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)
    stbt.press("KEY_1", timeBeforePress)
    stbt.press("KEY_2", timeBeforePress)
    stbt.press("KEY_5", timeBeforePress)
    stbt.press("KEY_7", timeBeforePress)
    stbt.press("KEY_INFO", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)

""" Procedura wykonujaca sekwencje krokow przechodzaca proces pierwszej instalacji
    warunki poczatkowe:
        W dekoderze zosataly wlasnie zrobione ustawienia fabryczne lub dekoder wyswietla ekran "Pierwsza Instalacja". """
def pierwszaInstalacja():
    stbt.wait_for_match("images/t1/first_installation_image.png", rebootWaitingTime)
    stbt.press("KEY_OK", timeBeforePress)
    stbt.wait_for_match("images/t1/searching_chanels_done_image.png", searchingChanelsTime)
    stbt.press("KEY_OK", timeBeforePress)
    stbt.press("KEY_BACK", afterChanelsConfirmedTime)
    stbt.press("KEY_OK", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)
    stbt.press("KEY_OK", timeBeforePress)

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
        - 0 - jesli tekst w danym regionie zniknie przed maksymalna liczba prob
        - -1 - jesli tekst w danym regionie NIE zniknie przed maksymalna liczba prob """
def myWaitWhileMatchText(text, region = stbt.Region.ALL, maxAttempts = 30, sleepTime = 1):
    counter = 0;
    result = stbt.match_text(text, None, region)
    while result.match == True and counter <= maxAttempts:
        time.sleep(sleepTime)
        counter += 1
        result = stbt.match_text(text, None, region)
    if counter > maxAttempts:
        return -1
    return 0

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

""" Procedura wczytujaca parametry testu z pliku konfiguracyjnego XML
    warunki poczatkowe:
        Plik konfiguracyjny zapisany jest w formacie XML oraz posiada z gory ustalona strukture.

    argumenty:
        - path - sciezka do pliku konfiguracyjnego """
def loadConfiguration(path):
    domTree = minidom.parse(path)
    parameters = domTree.firstChild # <parameters>
    paramChilds = parameters.childNodes
    
    soft = paramChilds[1] # <soft>
    softVersion = soft.childNodes
    currentUpdateVersions.append(int(soft.childNodes[1].firstChild.data)) # <version>
    currentUpdateVersions.append(int(soft.childNodes[3].firstChild.data)) # <version>
    
    signal = paramChilds[3] # <signal>
    signalChilds = signal.childNodes
    minSignalLevel = int(signal.childNodes[1].firstChild.data) # <min_level>
    minSignalQuality = int(signal.childNodes[3].firstChild.data) # <min_quality>

    network = paramChilds[5] # <network>
    wifi = network.childNodes
    minWiFiSignalLevel = int(network.childNodes[1].firstChild.data) # <min_wifi_level>

    testChannels = paramChilds[7] # <test_channels>
    channels = testChannels.childNodes
    mainTestChannels.append(int(testChannels.childNodes[1].firstChild.data)) # <channel>
    mainTestChannels.append(int(testChannels.childNodes[3].firstChild.data)) # <channel>
    mainTestChannels.append(int(testChannels.childNodes[5].firstChild.data)) # <channel>
    mainTestChannels.append(int(testChannels.childNodes[7].firstChild.data)) # <channel>
    alternativeTestChannels.append(int(testChannels.childNodes[9].firstChild.data)) # <channel>
    alternativeTestChannels.append(int(testChannels.childNodes[11].firstChild.data)) # <channel>
    alternativeTestChannels.append(int(testChannels.childNodes[13].firstChild.data)) # <channel>
    alternativeTestChannels.append(int(testChannels.childNodes[15].firstChild.data)) # <channel>
    
    """print(currentUpdateVersions)
    print(minSignalLevel)
    print(minSignalQuality)
    print(minWiFiSignalLevel)
    print(mainTestChannels)
    print(alternativeTestChannels)"""

def test_bash():
    print("POCZATEK")
    #subprocess.Popen(["ls"],shell=True, cwd = "./")
    #print(" ")
    #subprocess.Popen(["ls"],shell=True, cwd="/var/lib/stbt/test-pack/tests")
    #subprocess.Popen(["ls"],shell=True, cwd = "/etc/")
    #print(subprocess.Popen(["mount", "-t", "smbfs", "/10.30.5.154/share", "/mnt/10.30.5.154/share"], shell=True, cwd= "/"))
    print("KONIEC")

def test_ocr():
    text = stbt.ocr(region = stbt.Region(x=101, y=135, width=1075, height=32))
    print("POCZATEK")
    print(text)
    if text == "":
        print("OK")
    else:
        print("NOK")
    print("KONIEC")

def test_jakis():
    print("Rozpczecie testu.")
    stbt.match_text("RACHUNEK")
    #stbt.wait_for_match("./images/t1/no_bill_image.png", 5, region = stbt.Region(x=856, y=102, width=336, height=261))
    print("Koniec testu.")

""" Glowna procedura uruchamiajaca test dekodera po wybraniu odpowiedniego modelu"""
def test_glowny():
    while True:
        print("Wybierz model do przetestowania")
        print("1) DSI W74")
        print("2) HDS 7241/91")
        print("3) HDS 7241/91 CD")
        print("4) NCP 4740SF")
        print("5) ADB 2849")
        print("6) ADB 2850ST")
        print("7) ADB 2851S")
        print("8) ADB 3740SX")
        print("9) Wyjscie")
        
        case = input("Wybor: ")
        print("Wybrano " + case)

        switch = [
            TestDSIW74("/var/lib/stbt/test-pack/tests/test_config.xml"),
            2,
            3,
            4,
            5,
            TestADB2850ST("/var/lib/stbt/test-pack/tests/test_config_adb_3740sx.xml", "2850ST"),
            TestADB2850ST("/var/lib/stbt/test-pack/tests/test_config_adb_3740sx.xml", "2851S"),
            TestADB3740SX("/var/lib/stbt/test-pack/tests/test_config_adb_3740sx.xml", "3740SX"),
            9
        ]
        
        if case >= 1 and case <= 8:
            test = switch[case - 1]
            test.start()
        elif case == 9:
            exit()
        else:
            print("Blad! Wybierz liczbe calkowita z przedzialu od 1 do 9.")

        """c = int(choice)
        if c == 1:
            test = TestDSIW74("/var/lib/stbt/test-pack/tests/test_config.xml")
            test.start()
        elif c == 2:
            pass
        elif c == 3:
            pass
        elif c == 4:
            pass
        elif c == 5:
            pass
        elif c == 6:
            pass
        elif c == 7:
            pass
        elif c == 8:
            pass
        elif c == 9:
            break
        else:
            print("Blad! Wybierz liczbe calkowita od 1 do 9.")"""