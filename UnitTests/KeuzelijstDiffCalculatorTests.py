import copy
import unittest

from KeuzeLijstCreator import Keuzelijst, KeuzelijstWaarde
from KeuzelijstDiffCalculator import KeuzelijstDiffCalculator

branches = {
    'aim': 'aim',
    'prd': 'master'
}

eersteLijstPrd = Keuzelijst(label='label', definitie='definitie', notitie='notitie', objectUri='kl1')
eersteLijstPrd.keuzelijstWaardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2')}

eersteLijstAim = Keuzelijst(label='label', definitie='definitie', notitie='notitie', objectUri='kl1')
eersteLijstAim.keuzelijstWaardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1')}


class KeuzelijstDiffCalculatorTests(unittest.TestCase):
    def test_calculate_differences_identiek(self):
        testcalculator_identiek = KeuzelijstDiffCalculator(branches)
        testcalculator_identiek.keuzelijsten['prd'] = {}
        testcalculator_identiek.keuzelijsten['prd']['kl1'] = eersteLijstPrd

        testcalculator_identiek.keuzelijsten['aim'] = {}
        testcalculator_identiek.keuzelijsten['aim']['kl1'] = eersteLijstPrd

        result = testcalculator_identiek.calculate_differences()
        self.assertEqual(0, len(result))

    def test_calculate_differences_ontbrekende_waarde(self):
        testcalculator_ontbrekende_waarde = KeuzelijstDiffCalculator(branches)
        testcalculator_ontbrekende_waarde.keuzelijsten['prd'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['prd']['kl1'] = eersteLijstPrd

        testcalculator_ontbrekende_waarde.keuzelijsten['aim'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['aim']['kl1'] = eersteLijstAim

        result = testcalculator_ontbrekende_waarde.calculate_differences()
        self.assertEqual(1, len(result))
