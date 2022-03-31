import copy
import unittest

from KeuzeLijstCreator import Keuzelijst, KeuzelijstWaarde
from KeuzelijstDiffCalculator import KeuzelijstDiffCalculator

branches = {
            'aim': 'aim',
            'prd': 'master'
        }
testcalculator_identiek = KeuzelijstDiffCalculator(branches)
identiekeLijst = Keuzelijst(label='label', definitie='definitie', notitie='notitie', objectUri='kl1')
identiekeLijst.keuzelijstWaardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2')}

testcalculator_identiek.keuzelijsten['prd'] = {}
testcalculator_identiek.keuzelijsten['prd']['kl1'] = identiekeLijst

testcalculator_identiek.keuzelijsten['aim'] = {}
testcalculator_identiek.keuzelijsten['aim']['kl1'] = identiekeLijst

testcalculator_ontbrekende_waarde = copy.deepcopy(testcalculator_identiek)
testcalculator_ontbrekende_waarde.keuzelijsten['aim']['kl1'].keuzelijstWaardes.pop('uri2')


class KeuzelijstDiffCalculatorTests(unittest.TestCase):
    def test_calculate_differences_identiek(self):
        result = testcalculator_identiek.calculate_differences()
        self.assertEqual(0, len(result))

    def test_calculate_differences_ontbrekende_waarde(self):
        result = testcalculator_identiek.calculate_differences()
        self.assertEqual(1, len(result))
