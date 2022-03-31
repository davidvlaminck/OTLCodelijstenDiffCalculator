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

tweedeLijstPrd = Keuzelijst(label='label', definitie='definitie', notitie='notitie', objectUri='kl2')
tweedeLijstPrd.keuzelijstWaardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2')}

eersteLijstAim = Keuzelijst(label='label', definitie='definitie', notitie='notitie', objectUri='kl1')
eersteLijstAim.keuzelijstWaardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2')}

tweedeLijstAim = Keuzelijst(label='label', definitie='definitie', notitie='notitie', objectUri='kl2')
tweedeLijstAim.keuzelijstWaardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1')}

derdeLijstAim = Keuzelijst(label='label', definitie='definitie', notitie='notitie', objectUri='kl2')
derdeLijstAim.keuzelijstWaardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2'),
    'uri3': KeuzelijstWaarde(label='waarde3', definitie='definitie3', objectUri='uri3', invulwaarde='invulwaarde3')}


class KeuzelijstDiffCalculatorTests(unittest.TestCase):
    def test_calculate_differences_identiek(self):
        testcalculator_identiek = KeuzelijstDiffCalculator(branches)
        testcalculator_identiek.keuzelijsten['prd'] = {}
        testcalculator_identiek.keuzelijsten['prd']['kl1'] = copy.deepcopy(eersteLijstPrd)

        testcalculator_identiek.keuzelijsten['aim'] = {}
        testcalculator_identiek.keuzelijsten['aim']['kl1'] = copy.deepcopy(eersteLijstAim)

        result = testcalculator_identiek.calculate_differences()
        self.assertEqual(0, len(result))

    def test_calculate_differences_ontbrekende_waarde_in_aim(self):
        testcalculator_ontbrekende_waarde = KeuzelijstDiffCalculator(branches)
        testcalculator_ontbrekende_waarde.keuzelijsten['prd'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['prd']['kl2'] = copy.deepcopy(tweedeLijstPrd)

        testcalculator_ontbrekende_waarde.keuzelijsten['aim'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['aim']['kl2'] = copy.deepcopy(tweedeLijstAim)

        result = testcalculator_ontbrekende_waarde.calculate_differences()
        self.assertEqual(1, len(result))
        self.assertEqual('aim ontbreekt een waarde in keuzelijst', result[0][0])

    def test_calculate_differences_ontbrekende_waarde_in_prd(self):
        testcalculator_ontbrekende_waarde = KeuzelijstDiffCalculator(branches)
        testcalculator_ontbrekende_waarde.keuzelijsten['prd'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['prd']['kl2'] = copy.deepcopy(tweedeLijstPrd)

        testcalculator_ontbrekende_waarde.keuzelijsten['aim'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['aim']['kl2'] = copy.deepcopy(derdeLijstAim)

        result = testcalculator_ontbrekende_waarde.calculate_differences()
        self.assertEqual(1, len(result))
        self.assertEqual('prd ontbreekt een waarde in keuzelijst', result[0][0])

    def test_calculate_differences_ontbrekende_keuzelijst_in_aim(self):
        testcalculator_ontbrekende_waarde = KeuzelijstDiffCalculator(branches)
        testcalculator_ontbrekende_waarde.keuzelijsten['prd'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['prd']['kl1'] = copy.deepcopy(eersteLijstPrd)
        testcalculator_ontbrekende_waarde.keuzelijsten['prd']['kl2'] = copy.deepcopy(tweedeLijstPrd)

        testcalculator_ontbrekende_waarde.keuzelijsten['aim'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['aim']['kl1'] = copy.deepcopy(eersteLijstAim)

        result = testcalculator_ontbrekende_waarde.calculate_differences()
        self.assertEqual(1, len(result))
        self.assertEqual('aim ontbreekt een keuzelijst', result[0][0])

    def test_calculate_differences_ontbrekende_keuzelijst_in_prd(self):
        testcalculator_ontbrekende_waarde = KeuzelijstDiffCalculator(branches)
        testcalculator_ontbrekende_waarde.keuzelijsten['prd'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['prd']['kl1'] = copy.deepcopy(eersteLijstPrd)

        testcalculator_ontbrekende_waarde.keuzelijsten['aim'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['aim']['kl1'] = copy.deepcopy(eersteLijstAim)
        testcalculator_ontbrekende_waarde.keuzelijsten['aim']['kl2'] = copy.deepcopy(tweedeLijstAim)

        result = testcalculator_ontbrekende_waarde.calculate_differences()
        self.assertEqual(1, len(result))
        self.assertEqual('prd ontbreekt een keuzelijst', result[0][0])