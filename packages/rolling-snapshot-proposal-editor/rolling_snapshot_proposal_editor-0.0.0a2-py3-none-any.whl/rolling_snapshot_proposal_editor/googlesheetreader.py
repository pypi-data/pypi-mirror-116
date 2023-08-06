class GoogleSheetReader:
    """
    This class handles reading Google Spreadsheet directly using Google API.
    #####
    Usage:
    ???
    #####
    Ref:
    ???
    """
    def __init__(self,scopes,sheetid,rangename,credential,verbal=True):
        self.scopes = scopes
        self.sheetid = sheetid
        self.rangename = rangename
        self.credential = credential
        self.verbal = verbal
        if self.verbal: print('Use self.read() to read the sheet.\n')
    ####################
    ####################
    ####################
    # from https://developers.google.com/sheets/api/quickstart/python
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    import pandas as pd
    
    def read():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential,scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheetid,
                                    range=rangename).execute()
        values = result.get('values', [])

        ##### organize in pandas
        df = pd.DataFrame(values)
        df.columns = df.iloc[0]
        df.drop(df.index[0],inplace=True)
        self.df = df
        if self.verbal: print('Access the sheet by self.df ...\n')
    ####################
    ####################
    ####################
    