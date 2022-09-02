import datetime
import shutil

from KeuzelijstDiffCalculator import KeuzelijstDiffCalculator
from SheetsCell import SheetsCell
from SheetsWrapper import SheetsWrapper


if __name__ == '__main__':
    branches = {
        'prd': 'master',
        'tei': 'test',
        'aim': 'aim'
    }

    temp_dir_path = 'C:\\temp'

    calculator = KeuzelijstDiffCalculator(branches)
    calculator.download_lists(temp_dir_path)
    calculator.convert_branches_to_keuzelijsten()
    differences = calculator.calculate_differences()

    lines_to_write = [[f'Verschillen rapport gemaakt op {datetime.datetime.now()}'], [], ['omgeving','omschrijving verschil','uri object','uri keuzelijstwaarde (indien van toepassing)', 'waarde prd', 'waarde omgeving']]
    lines_to_write.extend(differences)

    sheetsWrapper = SheetsWrapper(service_cred_path='C:\\resources\\driven-wonder-149715-ca8bdf010930.json',
                                  readonly_scope=False)

    start_cell_str = 'A4'
    end_cell_str = sheetsWrapper.find_first_empty_row_from_starting_cell(spreadsheet_id='14PwD7_mHJ7lZbBOBfPvejxm5-uwuFzxvQySHKgzxoOk',
                                                                         sheet_name='overzicht',
                                                                         start_cell=start_cell_str)
    end_cell = SheetsCell(end_cell_str)
    end_cell.update_column_by_adding_number(5)
    range = start_cell_str + ':' + end_cell.cell
    sheetsWrapper.clear_cells_within_range(spreadsheet_id='14PwD7_mHJ7lZbBOBfPvejxm5-uwuFzxvQySHKgzxoOk',
                                           sheet_name='overzicht',
                                           sheetrange=range)

    sheetsWrapper.write_data_to_sheet(spreadsheet_id='14PwD7_mHJ7lZbBOBfPvejxm5-uwuFzxvQySHKgzxoOk',
                                      sheet_name='overzicht',
                                      start_cell='A1',
                                      data=lines_to_write)

    for branch in branches:
        shutil.rmtree(temp_dir_path + '\\' + branch)
