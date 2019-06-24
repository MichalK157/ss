from test_adb import TestADB
from test import Test
import time

class TestADB2850ST(TestADB):

    def __init__(self, configPath, model):
        self.loadConfiguration(configPath, model)
		
	def testDiody(self):
		print("Czy dioda swieci na zielono?")
        print("1) Tak")
        print("2) Nie")
        result = input()
        r = int(result)
        if r == 2:
            self.testsResults["daiode"] = False
            return
		stbt.press("KEY_POWER", Test.timeBeforePress)
		print("Czy dioda swieci na czerwono?")
        print("1) Tak")
        print("2) Nie")
        result = input()
        r = int(result)
        if r == 2:
            self.testsResults["daiode"] = False
            return
		self.testsResults["daiode"] = True
		stbt.press("KEY_POWER", Test.timeBeforePress)