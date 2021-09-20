#  EasyShifts (Python)
#  Written by Eran Meir    

![Empty](https://github.com/Eran-Meir/EasyShifts/blob/main/Empty.jpg)
![Options](https://github.com/Eran-Meir/EasyShifts/blob/main/Monthly%20Options.jpg)


## Installation
### Install the Google client library
To install the Google client library for Python, run the following command:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### First time running
If this is your first time running the project, it opens a new window prompting you to authorize access to your data:

If you are not already signed in to your Google account, you are prompted to sign in. If you are signed in to multiple Google accounts, you are asked to select one account to use for the authorization.

Note: Authorization information is stored on the file system, so subsequent executions don't prompt for authorization.
Click Accept. The app is authorized to access your data.

### OAuth 2.0 scope information
You can use the [Google Sheets API](https://developers.google.com/sheets/api/guides/authorizing) to view the auth access you need.
For reading and writing data we'll use ```auth/spreadsheets``` access
