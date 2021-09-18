from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from DayOptions import DayOptions


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']  # If modified delete the file token.json.
SPREADSHEET_ID = '1zfobZu4-Od4jCZ-nAjwq9klL_FwPMAgsVky5qRFbIZY'     # Spreadsheed ID (take it from its link)
SHEET_NAME_OPTIONS = 'Possibilities'                                # Sheet name
OPTIONS_DATA_CELLS = 'A1:AC36'                                      # From here we get the options data
SHEET_NAME_CURRENT_MONTH = 'CurrentMonth'                           # Sheet name
CURRENT_MONTH_UPDATE_CELLS = 'A1:H21'                               # In these cells we set the names of workers
CURRENT_MONTH_BALANCE_CELLS = 'J3:O11'                              # Total shifts data
OPTIONS_RANGE = SHEET_NAME_OPTIONS + '!' + OPTIONS_DATA_CELLS       # The work options
CURRENT_MONTH_UPDATE_RANGE = SHEET_NAME_CURRENT_MONTH + '!' + CURRENT_MONTH_UPDATE_CELLS    # Update range
CURRENT_MONTH_BALANCE_RANGE = SHEET_NAME_CURRENT_MONTH + '!' + CURRENT_MONTH_BALANCE_CELLS  # Balance range
DATE_REFERENCE = 'Date'             # Change this variable according to the type column in the sheet
MORNING_REFERENCE = 'Morning'       # Change this variable according to the type column in the sheet
NOON_REFERENCE = 'Noon'             # Change this variable according to the type column in the sheet
NIGHT_REFERENCE = 'Night'           # Change this variable according to the type column in the sheet
OPTIONS_DATE_CELLS_INCREMENT = 4    # Number of cells that contain each date
OPTIONS_COL_START_INDEX = 1             # Refers to the index in the list (starts from the B column)
OPTIONS_ROW_START_INDEX = 1         # Index of the first date row in values
OPTIONS_ROW_INCREMENT = 7           # Row increment
OPTIONS_SHIFT_ROW_COUNT = 6         # How many shift rows are there for each date?
MORNING_OFFSET_FROM_DATE = 1        # Rows between date and morning
NOON_OFFSET_FROM_DATE = 3           # Rows between date and noon
NIGHT_OFFSET_FROM_DATE = 5          # Rows between date and night
dayOptionsList = []                 # Will hold DayOptions objects


def main():
    createOptions()                 # Creating lists of options containing worker names
    #createEasyArrangement()         # Creating a work arrangement


def getOptionsData():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=OPTIONS_RANGE).execute()
    return result.get('values', [])


def assignCorrectShiftToSet(shiftRow, dayOption, shiftColStart, shiftColEnd):
    if len(shiftRow) >= shiftColEnd:
        cell = shiftRow[0]
        if cell == MORNING_REFERENCE:
            dayOption.addToMorningOptionsList(shiftRow[shiftColStart:shiftColEnd+1])
        elif cell == NOON_REFERENCE:
            dayOption.addToNoonOptionsList(shiftRow[shiftColStart:shiftColEnd+1])
        elif cell == NIGHT_REFERENCE:
            dayOption.addToNightOptionsList(shiftRow[shiftColStart:shiftColEnd+1])
    return dayOption


def populateShiftsLists(values):
    rowCounter = 0
    # Do this for every date row in values
    for row in values[OPTIONS_ROW_START_INDEX::OPTIONS_ROW_INCREMENT]:
        shiftRowStart = OPTIONS_ROW_START_INDEX + 1 + rowCounter*OPTIONS_ROW_INCREMENT
        shiftRowEnd = shiftRowStart + OPTIONS_SHIFT_ROW_COUNT - 1
        shiftColStart = OPTIONS_COL_START_INDEX
        shiftColEnd = shiftColStart + OPTIONS_DATE_CELLS_INCREMENT - 1
        if row is not None and len(row) > 0:
            for date in row[OPTIONS_COL_START_INDEX::OPTIONS_DATE_CELLS_INCREMENT]:
                dayOption = DayOptions(date)
                # Now for for the current day options block retrieve the day data
                for shiftRow in values[shiftRowStart:shiftRowEnd+1]:
                    if shiftRow is not None and len(shiftRow) > 0:
                        resultDayOption = assignCorrectShiftToSet(shiftRow, dayOption, shiftColStart, shiftColEnd)
                shiftColStart += OPTIONS_DATE_CELLS_INCREMENT
                shiftColEnd = shiftColStart + OPTIONS_DATE_CELLS_INCREMENT - 1
                resultDayOption.clearNullStringFromSets()
                dayOptionsList.append(resultDayOption)
        rowCounter += 1





def createOptions():
    values = getOptionsData()           # Get the data from the sheets
    if not values:
        print('ERROR: No data found.')  # No data found
    else:
        populateShiftsLists(values)     # Found data, populate the shifts
    for option in dayOptionsList:
        print(option.__dict__)
    for row in values:
        print(row)

if __name__ == '__main__':
    main()

#def createDayOptions