from __future__ import print_function
import os.path
from operator import itemgetter
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from DayOptions import DayOptions
from WorkDay import WorkDay

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']           # If modified delete the file token.json.
SPREADSHEET_ID = '1zfobZu4-Od4jCZ-nAjwq9klL_FwPMAgsVky5qRFbIZY'     # Spreadsheed ID (take it from its link)
SHEET_NAME_OPTIONS = 'Possibilities'                                # Sheet name
OPTIONS_DATA_CELLS = 'A1:AC36'                                      # From here we get the options data
SHEET_NAME_CURRENT_MONTH = 'CurrentMonth'                           # Sheet name
CURRENT_MONTH_UPDATE_CELLS = 'A1:H21'                               # In these cells we set the names of workers
CURRENT_MONTH_BALANCE_CELLS = 'J4:O11'                              # Total shifts data
OPTIONS_RANGE = SHEET_NAME_OPTIONS + '!' + OPTIONS_DATA_CELLS       # The work options
CURRENT_MONTH_UPDATE_RANGE = SHEET_NAME_CURRENT_MONTH + '!' + CURRENT_MONTH_UPDATE_CELLS    # Update range
CURRENT_MONTH_BALANCE_RANGE = SHEET_NAME_CURRENT_MONTH + '!' + CURRENT_MONTH_BALANCE_CELLS  # Balance range
DATE_REFERENCE = 'Date'             # Change this variable according to the type column in the sheet
MORNING_REFERENCE = 'Morning'       # Change this variable according to the type column in the sheet
NOON_REFERENCE = 'Noon'             # Change this variable according to the type column in the sheet
NIGHT_REFERENCE = 'Night'           # Change this variable according to the type column in the sheet
OPTIONS_DATE_CELLS_INCREMENT = 4    # Number of cells that contain each date
OPTIONS_COL_START_INDEX = 1         # Refers to the index in the list (starts from the B column)
OPTIONS_ROW_START_INDEX = 1         # Index of the first date row in values
OPTIONS_ROW_INCREMENT = 7           # Row increment
OPTIONS_SHIFT_ROW_COUNT = 6         # How many shift rows are there for each date?
MORNING_OFFSET_FROM_DATE = 1        # Rows between date and morning
NOON_OFFSET_FROM_DATE = 3           # Rows between date and noon
NIGHT_OFFSET_FROM_DATE = 5          # Rows between date and night
BALANCE_NAME_INDEX = 0              # 0 = Worker's name
BALANCE_MORNING_COUNT = 1           # 1 = Morning shifts count
BALANCE_NOON_COUNT = 2              # 2 = Noon shifts count
BALANCE_NIGHT_COUNT = 3             # 3 = Noon shifts count
BALANCE_FRIDAY_COUNT = 4            # 4 = Friday shifts count
BALANCE_SATURDAY_COUNT = 5          # 5 = Saturday shifts count
WRITE_CELL_START_COL = 'B'          # First column of our writing destination
WRITE_CELL_START_ROW = 3            # First row of our writing destination
WRITE_CELL_INCREMENT = 4            # Distance between writing rows
DAYS_IN_A_WEEK = 7                  # How many days in our working week
balanceList = []                    # Will hole the balance list
dayOptionsList = []                 # Will hold DayOptions objects
debug = False


def main():
    createOptions()                 # dayOptionsList now contains list of DayOptions Object for each day in the month
    createEasyArrangement()         # Creating a work arrangement


# Connects to an online Google Sheet and stores the data rows in the list 'values'
def getOptionsData():
    return readDataFromSheet(OPTIONS_RANGE)


# Assign the correct data to the correct set in the DayOptions Object
def assignCorrectShiftToSet(shiftRow, dayOption, shiftColStart, shiftColEnd):
    if len(shiftRow) >= shiftColEnd:
        cell = shiftRow[0]
        if cell == MORNING_REFERENCE:
            dayOption.addToMorningOptionsSet(shiftRow[shiftColStart:shiftColEnd + 1])
        elif cell == NOON_REFERENCE:
            dayOption.addToNoonOptionsSet(shiftRow[shiftColStart:shiftColEnd + 1])
        elif cell == NIGHT_REFERENCE:
            dayOption.addToNightOptionsSet(shiftRow[shiftColStart:shiftColEnd + 1])
    return dayOption


# For each date row in values (5 week rows)
# Take each date in that row and create a shifts "block" with it's options
# This will result in creating a full DayOptions Object, and will be added to the list
def populateShiftsSets(values):
    rowCounter = 0
    # For every date row in values
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


# Get the options from the Possibilities Google Sheet
# Create a List of DayOptions Objects
def createOptions():
    values = getOptionsData()           # Get the data from the sheets
    if not values:
        print('ERROR: No data found.')  # No data found
    else:
        populateShiftsSets(values)      # Found data, populate the shifts
        print('*** Successfully created dayOptionsList')
    if debug:
        print("\n*** All DayOptions Objects data:")
        for option in dayOptionsList:
            print(option.__dict__)
        print("\n*** All values List:")
        for row in values:
            print(row)
        print("\n*** Balance List:")
        for row in balanceList:
            print(row)


# We have all the workers options in 'dayOptionsList' we can start assigning people to shifts
# For each date in our month assign a worker to each shift
# First assign the
def createEasyArrangement():
    count = 0
    workDay = None
    for dayOption in dayOptionsList:
        if isinstance(dayOption, DayOptions):
            # The person who worked last night can't work today's morning
            if workDay is not None:
                lastNightWorker = workDay.getNightWorker()
                dayOption.morningOptionsSet.discard(lastNightWorker)
            # Create a new WorkDay object with our current date
            workDay = WorkDay(dayOption.getDate())
            assignShiftsToWorkDay(dayOption, workDay)
            cellRange = getCellRange(count)
            writeDataToSheet(workDay, cellRange)
            count += 1
            print(workDay.__dict__)

def getCellRange(count):
    colOffset = count % DAYS_IN_A_WEEK
    rowOffset = count // DAYS_IN_A_WEEK
    if colOffset == 0:
        col = WRITE_CELL_START_COL
    else:
        col = chr(ord(WRITE_CELL_START_COL) + colOffset)
    row = WRITE_CELL_START_ROW + WRITE_CELL_INCREMENT * rowOffset
    return str(col) + str(row)

def writeDataToSheet(workDay, cellRange):
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
    sheetValues = service.spreadsheets().values()
    writeData = workDay.getWriteData()
    print(writeData)
    value_range_body = {
        "majorDimension": "ROWS",
        "values": writeData
    }
    request = sheetValues.update(spreadsheetId=SPREADSHEET_ID,
                                 range=SHEET_NAME_CURRENT_MONTH + "!" + cellRange,
                                 valueInputOption='USER_ENTERED',
                                 body=value_range_body)
    response = request.execute()


# First we assign constraint shifts then we assign the rest
# In the end workDay should contain a
def assignShiftsToWorkDay(dayOption, workDay):
    assignConstraintShiftsFirst(dayOption, workDay)
    balanceList = getBalanceData()  # Get the current balance data
    shiftIndex = 0  # Sort according to morning
    assignShiftToWorkDay(dayOption, workDay, shiftIndex, balanceList)
    shiftIndex = 1  # Sort according to Noon
    assignShiftToWorkDay(dayOption, workDay, shiftIndex, balanceList)
    shiftIndex = 2  # Sort according to Night
    assignShiftToWorkDay(dayOption, workDay, shiftIndex, balanceList)


def assignShiftToWorkDay(dayOption, workDay, shiftIndex, balanceList):
    sortListsByLowestShiftIndex(balanceList, shiftIndex)
    if shiftIndex == 0:
        setList = list(dayOption.getMorningOptionsSet())
        if len(setList) > 0:
            workDay.setMorningWorker(setList[0])
    elif shiftIndex == 1:
        setList = list(dayOption.getNoonOptionsSet())
        if len(setList) > 0:
            workDay.setNoonWorker(setList[0])
    elif shiftIndex == 2:
        setList = list(dayOption.getNightOptionsSet())
        if len(setList) > 0:
            workDay.setNightWorker(setList[0])
    dayOption.removeWorkerFromDayIfAssigned(setList[0])


# We assign constrain shifts first for example if only one person can work the morning then we want him to do it
def assignConstraintShiftsFirst(dayOption, workDay):
    if len(dayOption.morningOptionsSet) == 1:
        worker = dayOption.morningOptionsSet[0]
        workDay.setMorningWorker(worker)
        dayOption.removeWorkerFromDayIfAssigned(worker)
    if len(dayOption.noonOptionsSet) == 1:
        worker = dayOption.noonOptionsSet[0]
        workDay.setNoonWorker(worker)
        dayOption.removeWorkerFromDayIfAssigned(worker)
    if len(dayOption.nightOptionsSet) == 1:
        worker = dayOption.nightOptionsSet[0]
        workDay.setNightWorker(worker)
        dayOption.removeWorkerFromDayIfAssigned(worker)

# Sorts in place the list according to the inner lists with column shiftIndex
def sortListsByLowestShiftIndex(balanceList, shiftIndex):
    balanceList.sort(key=lambda x: x[shiftIndex])


# Return a list with each worker's shifts balance count
# Index = Meaning
# 0     = Worker's name
# 1     = Morning shifts count
# 2     = Noon shifts count
# 3     = Night shifts count
# 4     = Friday shifts count
# 5     = Saturday shifts count
def getBalanceData():
    return readDataFromSheet(CURRENT_MONTH_BALANCE_RANGE)


# Returns a list of rows containing data from the specified range from inside the Google Sheet
def readDataFromSheet(dataRange):
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
                                range=dataRange).execute()
    return result.get('values', [])

if __name__ == '__main__':
    main()

