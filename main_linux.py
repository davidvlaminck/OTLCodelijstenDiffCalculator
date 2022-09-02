import datetime
import shutil

from KeuzelijstDiffCalculator import KeuzelijstDiffCalculator
from SheetsCell import SheetsCell
from SheetsWrapper import SheetsWrapper


def get_spocs(sheetsWrapper: SheetsWrapper):
    kl_eigenaar_sheet_id = '1we4yfj6HXhHuJ0LMsfYJ455PJfwf8SC6ZZC1Mre2KOM'
    kl_eigenaar_sheet_name = 'KL_PROD dd23/06/2022'

    start_cell_str = 'A2'
    end_cell_str = sheetsWrapper.find_first_empty_row_from_starting_cell(
        spreadsheet_id=kl_eigenaar_sheet_id, sheet_name=kl_eigenaar_sheet_name, start_cell=start_cell_str)
    end_cell_str = 'A562'
    end_cell = SheetsCell(end_cell_str)
    end_cell.update_column_by_adding_number(7)
    range = start_cell_str + ':' + end_cell.cell
    print(range)

    data = sheetsWrapper.read_data_from_sheet(spreadsheet_id=kl_eigenaar_sheet_id, sheet_name=kl_eigenaar_sheet_name,
                                              sheetrange=range)

    kl_eigenaar_dict = {}
    for row in data:
        if row[0] != '':
            kl_eigenaar_dict[row[0]] = (row[1], row[6])
    return kl_eigenaar_dict


if __name__ == '__main__':
    branches = {
        'prd': 'master',
        'tei': 'test',
        'aim': 'aim'
    }

    temp_dir_path = '/home/davidlinux/.tmp/'

    sheetsWrapper = SheetsWrapper(
        service_cred_path='/home/davidlinux/Documents/AWV/resources/driven-wonder-149715-ca8bdf010930.json',
        readonly_scope=False)

    kl_eigenaar_dict = get_spocs(sheetsWrapper)

    calculator = KeuzelijstDiffCalculator(branches)
    calculator.temp_dir_path = temp_dir_path
    # calculator.download_lists(temp_dir_path)
    calculator.convert_branches_to_keuzelijsten()
    differences = calculator.calculate_differences(kl_eigenaar_dict=kl_eigenaar_dict)

    overzicht_sheet_id = '14PwD7_mHJ7lZbBOBfPvejxm5-uwuFzxvQySHKgzxoOk'
    overzicht_sheet_name = 'overzicht'

    start_cell_str = 'A4'
    end_cell_str = sheetsWrapper.find_first_empty_row_from_starting_cell(spreadsheet_id=overzicht_sheet_id,
                                                                         sheet_name=overzicht_sheet_name,
                                                                         start_cell=start_cell_str)
    end_cell = SheetsCell(end_cell_str)
    end_cell.update_column_by_adding_number(10)
    range = start_cell_str + ':' + end_cell.cell

    existing_data = sheetsWrapper.read_data_from_sheet(spreadsheet_id=overzicht_sheet_id,
                                                       sheet_name=overzicht_sheet_name, sheetrange=range)

    differences = calculator.update_differences_with_persistent_data(differences, existing_data)

    sheetsWrapper.clear_cells_within_range(spreadsheet_id=overzicht_sheet_id, sheet_name=overzicht_sheet_name,
                                           sheetrange=range)

    lines_to_write = [[f'Verschillen rapport gemaakt op {datetime.datetime.now()}'], []]
    lines_to_write.extend(differences)

    sheetsWrapper.write_data_to_sheet(spreadsheet_id=overzicht_sheet_id, sheet_name=overzicht_sheet_name,
                                      start_cell='A1', data=lines_to_write)

    start_sheetcell = SheetsCell('A3')
    sheetsWrapper.clear_filter(overzicht_sheet_id, overzicht_sheet_name)
    end_sheetcell = start_sheetcell.copy()
    end_sheetcell.update_column_by_adding_number(10)
    end_sheetcell.update_row_by_adding_number(len(differences) - 1)
    sheetsWrapper.create_basic_filter(overzicht_sheet_id, overzicht_sheet_name,
                                      f'{start_sheetcell.cell}:{end_sheetcell.cell}')

    # for branch in branches:
    #    shutil.rmtree(temp_dir_path + '\\' + branch)
