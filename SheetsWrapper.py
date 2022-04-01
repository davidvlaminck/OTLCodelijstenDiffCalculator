import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

from SheetsRange import SheetsRange


class SheetsWrapper:
    def __init__(self, service_cred_path: str = '', readonly_scope: None | bool = None):
        if service_cred_path == '':
            raise NotImplementedError('only access with service account is supported')
        self.service_cred_path = service_cred_path
        self.credentials: None | Credentials = None

        if readonly_scope is None:
            raise ValueError('set readonly_scope to True or False')

    def write_data_to_sheet(self, spreadsheet_id: str, sheet_name: str, range_start: str, data: list):
        credentials = self.authenticate()
        cell_range = self.calculate_cell_range_by_data(SheetsRange(range_start), data)
        service = build('sheets', 'v4', credentials=credentials)
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            valueInputOption='RAW',
            range=sheet_name + '!' + cell_range,
            body=dict(
                majorDimension='ROWS',
                values=data)
        ).execute()

    def authenticate(self) -> Credentials:
        if self.credentials is not None:
            return self.credentials

        cred_file_path = Path(self.service_cred_path)
        if not cred_file_path.is_file():
            raise FileNotFoundError(f"could not find the credentials file at {cred_file_path}")

        with open(cred_file_path) as cred_file:
            gcp_sa_credentials = json.load(cred_file)

        self.credentials = service_account.Credentials.from_service_account_info(gcp_sa_credentials)
        return self.credentials

    def calculate_cell_range_by_data(self, cell_start: SheetsRange, data: list = None):
        if cell_start is None:
            raise ValueError("range_start can't be empty")

        if len(data) == 0:
            raise ValueError("data can't be empty")

        cell_end = cell_start.copy()

        max_cells_in_row = max(map(lambda x: len(x), data))
        cell_end.update_column_by_adding_number(max_cells_in_row - 1)
        cell_end.update_row_by_adding_number(len(data) - 1)

        return cell_start.range + ':' + cell_end.range
