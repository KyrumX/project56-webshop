import unittest

from django.test import TestCase

# Create your tests here.
from store.collections.tools import TransBool


class ToolsTests(unittest.TestCase):
    #Method naming: MethodName_Scenario_ExpectedBehavior()...
    #Scenarios: all results/execution paths

    def test_TransBool_BoolIsTrue_ReturnsJa(self):
        #Arrange
        testinput = True

        #Act
        result = TransBool(testinput)

        #Assert
        self.assertEqual("Ja", result)

    def test_TransBool_BoolIsFalse_ReturnsNee(self):
        testinput = False

        result = TransBool(testinput)

        self.assertEqual("Nee", result)

    def test_TransBool_OtherTypeIsGiven_ReturnsNee(self):
        testinput = "A string"

        result = TransBool(testinput)

        self.assertEqual("Nee", result)