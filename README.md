#  EasyShifts (Python)
#  Written by Eran Meir    

![Empty](https://github.com/Eran-Meir/EasyShifts/blob/main/Empty.jpg)
![Presentation](https://github.com/Eran-Meir/EasyShifts/blob/main/EasyShifts.gif)

## About this project
### Motivation
Creating 24/7 shifts is not always an easy task.

This Python project can both help saving time while also making people happy!
But how? Well, it simply does the task for you and the shifts are almost equally shared between team members

### How it works
There are certain constraints:
- Team members will be assigned only to shifts they flagged as suiteable for them
- If only one person can work a certain shift then he'll be the one to do it (duty calls!)
- A team member will not work in the following morning if he has worked in the night before

## Installation
Most of this part is taken from Google Sheets API and the credit goes to Google.
Please refer to [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) if you're struggling with Installation

### Install the Google client library
To install the Google client library for Python, run the following command:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### First time running
If this is your first time running the project, it opens a new window prompting you to authorize access to your data

If you are not already signed in to your Google account, you are prompted to sign in. If you are signed in to multiple Google accounts, you are asked to select one account to use for the authorization.

Note: Authorization information is stored on the file system, so subsequent executions don't prompt for authorization.
Click Accept. The app is authorized to access your data.

### Prerequisites
To run this project, you need the following prerequisites:

- Python 2.6 or greater.
- The pip package management tool
- A Google Cloud Platform project with the API enabled. To create a project and enable an API, refer to: [Create a project and enable the API](https://developers.google.com/workspace/guides/create-project)
- Enabling the "Google Sheets API".
- Authorization credentials for a desktop application. To learn how to create credentials for a desktop application, refer to [Create credentials](https://developers.google.com/workspace/guides/create-credentials).
- A Google account.

### OAuth 2.0 scope information
You can use the [Google Sheets API](https://developers.google.com/sheets/api/guides/authorizing) to view the auth access you need.
For reading and writing data we'll use ```auth/spreadsheets``` access
