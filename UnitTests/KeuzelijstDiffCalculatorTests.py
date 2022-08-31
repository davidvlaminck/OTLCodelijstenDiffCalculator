import copy
import unittest

from KeuzeLijstCreator import Keuzelijst, KeuzelijstWaarde
from KeuzelijstDiffCalculator import KeuzelijstDiffCalculator

branches = {
    'aim': 'aim',
    'prd': 'master'
}

eersteLijstPrd = Keuzelijst(label='label', definitie='definitie', objectUri='kl1')
eersteLijstPrd.keuzelijst_waardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2')}

tweedeLijstPrd = Keuzelijst(label='label', definitie='definitie', objectUri='kl2')
tweedeLijstPrd.keuzelijst_waardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2')}

eersteLijstAim = Keuzelijst(label='label', definitie='definitie', objectUri='kl1')
eersteLijstAim.keuzelijst_waardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2')}

tweedeLijstAim = Keuzelijst(label='label', definitie='definitie', objectUri='kl2')
tweedeLijstAim.keuzelijst_waardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1')}

derdeLijstAim = Keuzelijst(label='label', definitie='definitie', objectUri='kl2')
derdeLijstAim.keuzelijst_waardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2'),
    'uri3': KeuzelijstWaarde(label='waarde3', definitie='definitie3', objectUri='uri3', invulwaarde='invulwaarde3')}

vierdeLijstAim = Keuzelijst(label='label_aangepast', definitie='definitie_aangepast', objectUri='kl1')
vierdeLijstAim.keuzelijst_waardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2', definitie='definitie2', objectUri='uri2', invulwaarde='invulwaarde2')}

vijfdeLijstAim = Keuzelijst(label='label', definitie='definitie', objectUri='kl1')
vijfdeLijstAim.keuzelijst_waardes = {
    'uri1': KeuzelijstWaarde(label='waarde1', definitie='definitie1', objectUri='uri1', invulwaarde='invulwaarde1'),
    'uri2': KeuzelijstWaarde(label='waarde2_aangepast', definitie='definitie2_aangepast', objectUri='uri2', invulwaarde='invulwaarde2_aangepast')}


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
        self.assertEqual('prd heeft een waarde in een keuzelijst die niet bestaat op aim', result[0][1])

    def test_calculate_differences_ontbrekende_waarde_in_prd(self):
        testcalculator_ontbrekende_waarde = KeuzelijstDiffCalculator(branches)
        testcalculator_ontbrekende_waarde.keuzelijsten['prd'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['prd']['kl2'] = copy.deepcopy(tweedeLijstPrd)

        testcalculator_ontbrekende_waarde.keuzelijsten['aim'] = {}
        testcalculator_ontbrekende_waarde.keuzelijsten['aim']['kl2'] = copy.deepcopy(derdeLijstAim)

        result = testcalculator_ontbrekende_waarde.calculate_differences()
        self.assertEqual(1, len(result))
        self.assertEqual('prd ontbreekt een waarde in keuzelijst t.o.v. aim', result[0][1])

    def test_calculate_differences_ontbrekende_keuzelijst_in_aim(self):
        testcalculator_ontbrekende_keuzelijst = KeuzelijstDiffCalculator(branches)
        testcalculator_ontbrekende_keuzelijst.keuzelijsten['prd'] = {}
        testcalculator_ontbrekende_keuzelijst.keuzelijsten['prd']['kl1'] = copy.deepcopy(eersteLijstPrd)
        testcalculator_ontbrekende_keuzelijst.keuzelijsten['prd']['kl2'] = copy.deepcopy(tweedeLijstPrd)

        testcalculator_ontbrekende_keuzelijst.keuzelijsten['aim'] = {}
        testcalculator_ontbrekende_keuzelijst.keuzelijsten['aim']['kl1'] = copy.deepcopy(eersteLijstAim)

        result = testcalculator_ontbrekende_keuzelijst.calculate_differences()
        self.assertEqual(1, len(result))
        self.assertEqual('prd heeft een keuzelijst die niet bestaat op aim', result[0][1])

    def test_calculate_differences_ontbrekende_keuzelijst_in_prd(self):
        testcalculator_ontbrekende_keuzelijst = KeuzelijstDiffCalculator(branches)
        testcalculator_ontbrekende_keuzelijst.keuzelijsten['prd'] = {}
        testcalculator_ontbrekende_keuzelijst.keuzelijsten['prd']['kl1'] = copy.deepcopy(eersteLijstPrd)

        testcalculator_ontbrekende_keuzelijst.keuzelijsten['aim'] = {}
        testcalculator_ontbrekende_keuzelijst.keuzelijsten['aim']['kl1'] = copy.deepcopy(eersteLijstAim)
        testcalculator_ontbrekende_keuzelijst.keuzelijsten['aim']['kl2'] = copy.deepcopy(tweedeLijstAim)

        result = testcalculator_ontbrekende_keuzelijst.calculate_differences()
        self.assertEqual(1, len(result))
        self.assertEqual('prd ontbreekt een keuzelijst t.o.v. aim', result[0][1])

    def test_calculate_differences_verschillen_in_keuzelijst(self):
        testcalculator_verschillende_keuzelijst = KeuzelijstDiffCalculator(branches)
        testcalculator_verschillende_keuzelijst.keuzelijsten['prd'] = {}
        testcalculator_verschillende_keuzelijst.keuzelijsten['prd']['kl1'] = copy.deepcopy(eersteLijstPrd)

        testcalculator_verschillende_keuzelijst.keuzelijsten['aim'] = {}
        testcalculator_verschillende_keuzelijst.keuzelijsten['aim']['kl1'] = copy.deepcopy(vierdeLijstAim)

        result = testcalculator_verschillende_keuzelijst.calculate_differences()
        self.assertEqual(2, len(result))
        self.assertEqual('prd en aim keuzelijst verschillen van label', result[0][1])
        self.assertEqual('prd en aim keuzelijst verschillen van definitie', result[1][1])

    def test_calculate_differences_verschillen_in_keuzelijstwaardes(self):
        testcalculator_verschillende_keuzelijstwaardes = KeuzelijstDiffCalculator(branches)
        testcalculator_verschillende_keuzelijstwaardes.keuzelijsten['prd'] = {}
        testcalculator_verschillende_keuzelijstwaardes.keuzelijsten['prd']['kl1'] = copy.deepcopy(eersteLijstPrd)

        testcalculator_verschillende_keuzelijstwaardes.keuzelijsten['aim'] = {}
        testcalculator_verschillende_keuzelijstwaardes.keuzelijsten['aim']['kl1'] = copy.deepcopy(vijfdeLijstAim)

        result = testcalculator_verschillende_keuzelijstwaardes.calculate_differences()
        self.assertEqual(3, len(result))
        self.assertEqual('prd en aim keuzelijstwaarde verschillen van notatie', result[0][1])
        self.assertEqual('prd en aim keuzelijstwaarde verschillen van label', result[1][1])
        self.assertEqual('prd en aim keuzelijstwaarde verschillen van definitie', result[2][1])