import datetime

from GitHubDownloader import GitHubDownloader
from KeuzelijstDiffCalculator import KeuzelijstDiffCalculator
from SheetsWrapper import SheetsWrapper


if __name__ == '__main__':
    branches = {
        'aim': 'aim',
        'prd': 'master'
    }

    GitHubDownloader.download_all_branches(branches)

    calculator = KeuzelijstDiffCalculator(branches)
    calculator.convert_branches_to_keuzelijsten()
    differences = calculator.calculate_differences()

    lines_to_write = [[f'Verschillen rapport gemaakt op {datetime.datetime.now()}'], []]
    lines_to_write.extend(differences)

    sheetsWrapper = SheetsWrapper(service_cred_path='C:\\resources\\driven-wonder-149715-ca8bdf010930.json',
                                  readonly_scope=False)
    sheetsWrapper.write_data_to_sheet(spreadsheet_id='14PwD7_mHJ7lZbBOBfPvejxm5-uwuFzxvQySHKgzxoOk',
                                      sheet_name='overzicht',
                                      cell_start='A1',
                                      data=lines_to_write)