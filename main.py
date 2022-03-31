import datetime
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from KeuzelijstDiffCalculator import KeuzelijstDiffCalculator
from SheetsWrapper import SheetsWrapper

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '14PwD7_mHJ7lZbBOBfPvejxm5-uwuFzxvQySHKgzxoOk'
SAMPLE_RANGE_NAME = 'Blad1!A1:B2'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    service_cred_path = 'C:\\resources\\driven-wonder-149715-ca8bdf010930.json'

    with open(service_cred_path) as cred_file:
        gcp_sa_credentials = json.load(cred_file)

    credentials = service_account.Credentials.from_service_account_info(gcp_sa_credentials)

    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])


        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)

        response_date = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            valueInputOption='RAW',
            range=SAMPLE_RANGE_NAME,
            body=dict(
                majorDimension='ROWS',
                values=[['2','3'],['2']])
        ).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    branches = {
        'aim': 'aim',
        'prd': 'master'
    }
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

    pass