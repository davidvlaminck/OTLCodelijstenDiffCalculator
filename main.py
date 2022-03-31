import json
import os.path


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from GitHubDownloader import GitHubDownloader
from KeuzeLijstCreator import KeuzelijstCreator
from KeuzelijstDiffCalculator import KeuzelijstDiffCalculator

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1TxiT8eRqZfZz0VHN-lFbxVGrCEwCXRivKPTBQha_ccs'
SAMPLE_RANGE_NAME = 'Historiek!A3'


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
                values=[['2']])
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
    calculator.calculate_differences()