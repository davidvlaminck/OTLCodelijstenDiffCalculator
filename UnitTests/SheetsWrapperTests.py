import unittest

from SheetsRange import SheetsRange
from SheetsWrapper import SheetsWrapper


class SheetsWrapperTests(unittest.TestCase):
    def test_calculate_cell_range_no_cell_or_no_data(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)
        with self.assertRaises(ValueError):
            sheetsWrapper.calculate_cell_range(SheetsRange(''), [['']])
        with self.assertRaises(ValueError):
            sheetsWrapper.calculate_cell_range(SheetsRange('A1'), [])

    def test_calculate_cell_range_A1_1_cell(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)

        cell_range = sheetsWrapper.calculate_cell_range(SheetsRange('A1'), [['']])
        self.assertEqual('A1:A1', cell_range)

    def test_calculate_cell_range_A1_2_cells_in_1_row(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)

        cell_range = sheetsWrapper.calculate_cell_range(SheetsRange('A1'), [['', '']])
        self.assertEqual('A1:B1', cell_range)

    def test_calculate_cell_range_A1_2_cells_in_1_column(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)

        cell_range = sheetsWrapper.calculate_cell_range(SheetsRange('A1'), [[''], ['']])
        self.assertEqual('A1:A2', cell_range)
