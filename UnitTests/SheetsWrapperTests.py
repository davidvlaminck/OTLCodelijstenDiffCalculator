import unittest

from SheetsWrapper import SheetsWrapper


class SheetsWrapperTests(unittest.TestCase):
    def test_calculate_cell_range_no_cell_or_no_data(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)
        with self.assertRaises(ValueError):
            sheetsWrapper.calculate_cell_range('', [['']])
        with self.assertRaises(ValueError):
            sheetsWrapper.calculate_cell_range('A1', [])

    def test_calculate_cell_range_A1_1_cell(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)

        cell_range = sheetsWrapper.calculate_cell_range('A1', [['']])
        self.assertEqual('A1:A1', cell_range)

    def test_calculate_cell_range_A1_2_cells_in_1_row(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)

        cell_range = sheetsWrapper.calculate_cell_range('A1', [['', '']])
        self.assertEqual('A1:B1', cell_range)

    def test_calculate_cell_range_A1_2_cells_in_1_column(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)

        cell_range = sheetsWrapper.calculate_cell_range('A1', [[''], ['']])
        self.assertEqual('A1:A2', cell_range)

    def test_convert_number_to_column(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)
        with self.subTest('1 to A'):
            self.assertEqual('A', sheetsWrapper.convert_number_to_column(1))
        with self.subTest('2 to B'):
            self.assertEqual('B', sheetsWrapper.convert_number_to_column(2))
        with self.subTest('27 to AA'):
            self.assertEqual('AA', sheetsWrapper.convert_number_to_column(27))
        with self.subTest('28 to AB'):
            self.assertEqual('AB', sheetsWrapper.convert_number_to_column(28))
        with self.subTest('53 to BA'):
            self.assertEqual('BA', sheetsWrapper.convert_number_to_column(53))
        with self.subTest('702 to AB'):
            self.assertEqual('ZZ', sheetsWrapper.convert_number_to_column(702))
        with self.subTest('703 to AAA'):
            self.assertEqual('AAA', sheetsWrapper.convert_number_to_column(703))
        with self.subTest('729 to ABA'):
            self.assertEqual('ABA', sheetsWrapper.convert_number_to_column(729))
        with self.subTest('18278 to ZZZ'):
            self.assertEqual('ZZZ', sheetsWrapper.convert_number_to_column(18278))
        with self.subTest('invalid values'):
            with self.assertRaises(ValueError):
                sheetsWrapper.convert_number_to_column(18279)
            with self.assertRaises(ValueError):
                sheetsWrapper.convert_number_to_column(0)

    def test_convert_column_to_number(self):
        sheetsWrapper = SheetsWrapper(service_cred_path='a', readonly_scope=False)
        with self.subTest('A to 1'):
            self.assertEqual(1, sheetsWrapper.convert_column_to_number('A'))
        with self.subTest('B to 2'):
            self.assertEqual(2, sheetsWrapper.convert_column_to_number('B'))
        with self.subTest('Z to 26'):
            self.assertEqual(26, sheetsWrapper.convert_column_to_number('Z'))
        with self.subTest('AA to 27'):
            self.assertEqual(27, sheetsWrapper.convert_column_to_number('AA'))
        with self.subTest('BA to 53'):
            self.assertEqual(53, sheetsWrapper.convert_column_to_number('BA'))
        with self.subTest('ZZ to 702'):
            self.assertEqual(702, sheetsWrapper.convert_column_to_number('ZZ'))
        with self.subTest('AAA to 703'):
            self.assertEqual(703, sheetsWrapper.convert_column_to_number('AAA'))
        with self.subTest('ABA to 729'):
            self.assertEqual(729, sheetsWrapper.convert_column_to_number('ABA'))
        with self.subTest('ZZZ to 18278'):
            self.assertEqual(18278, sheetsWrapper.convert_column_to_number('ZZZ'))
        with self.subTest('invalid values'):
            with self.assertRaises(ValueError):
                sheetsWrapper.convert_column_to_number('')
            with self.assertRaises(ValueError):
                sheetsWrapper.convert_column_to_number('AAAA')