import json
import re
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account


class SheetsWrapper:
    def __init__(self, service_cred_path: str = '', readonly_scope: None | bool = None):
        if service_cred_path == '':
            raise NotImplementedError('only access with service account is supported')
        self.service_cred_path = service_cred_path

        if readonly_scope is None:
            raise ValueError('set readonly_scope to True or False')

    def write_data_to_sheet(self, spreadsheet_id, sheet_name, cell_start, data):
        credentials = self.authenticate()
        cell_range = self.calculate_cell_range(cell_start, data)
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
        cred_file_path = Path(self.service_cred_path)
        if not cred_file_path.is_file():
            raise FileNotFoundError(f"could not find the credentials file at {cred_file_path}")

        with open(cred_file_path) as cred_file:
            gcp_sa_credentials = json.load(cred_file)

        credentials = service_account.Credentials.from_service_account_info(gcp_sa_credentials)
        return credentials

    def calculate_cell_range(self, cell_start: str = '', data: list = []):
        if cell_start == '':
            raise ValueError("cell_start can't be empty")

        if data == []:
            raise ValueError("data can't be empty")

        column = re.split('\d', cell_start)[0]
        row = int(cell_start[len(column):])

        max_cells_in_row = max(map(lambda x: len(x), data))
        end_column = self.convert_number_to_column(self.convert_column_to_number(column) + max_cells_in_row - 1)
        end_row = row + len(data) - 1

        return cell_start + ':' + end_column + str(end_row)

    def convert_number_to_column(self, number: int) -> str:
        if number < 1 or number > 18278:
            raise ValueError

        first = (number - 1) % 26 + 1
        if number < 27:
            return chr(ord('@') + first)

        second = (int((number - 1) / 26) - 1) % 26 + 1
        if number < 703:
            return chr(ord('@') + second) + chr(ord('@') + first)

        third = (int((number - 27) / 676) - 1) % 26 + 1
        return chr(ord('@') + third) + chr(ord('@') + second) + chr(ord('@') + first)

    def convert_column_to_number(self, column: str) -> int:
        if len(column) < 1 or len(column) > 3:
            raise ValueError

        sum = 0
        for i, letter in enumerate(column[::-1]):
            sum += (ord(letter) - 64) * (26 ** i)

        return sum
