import pickle
import os
import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from GPU_ import GPU

def Create_Service(client_secret_file, api_name, api_version, *scopes, prefix=''):
	CLIENT_SECRET_FILE = client_secret_file
	API_SERVICE_NAME = api_name
	API_VERSION = api_version
	SCOPES = [scope for scope in scopes[0]]
	
	cred = None
	working_dir = os.getcwd()
	token_dir = 'token files'
	pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

	### Check if token dir exists first, if not, create the folder
	if not os.path.exists(os.path.join(working_dir, token_dir)):
		os.mkdir(os.path.join(working_dir, token_dir))

	if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
		with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
			cred = pickle.load(token)

	if not cred or not cred.valid:
		if cred and cred.expired and cred.refresh_token:
			cred.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
			cred = flow.run_local_server()

		with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
			pickle.dump(cred, token)

	try:
		service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
		# print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
		return service
	except Exception as e:
		print(e)
		print(f'Failed to create service instance for {API_SERVICE_NAME}')
		os.remove(os.path.join(working_dir, token_dir, pickle_file))
		return None 

def send_email(product: GPU):
    if not os.path.exists("client.json"):
        print("Please provide client.json")
        return False
    if not os.path.exists("email.txt"):
        print("Please provide email.txt")
        return False
    with open("email.txt", "r") as f:
        file = f.readlines()
        email_ = file[0].strip()
    CLIENT_FILE = 'client.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)
    
    emailMsg = f'''
    Price Alert!
    {product.get_title()}
    
    Price: {product.get_price()}
    Model: {product.get_model()}
    Stock: {product.get_stock()}
    
    {product.get_link()}
    
    From python script.
    '''
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = email_
    mimeMessage['subject'] = f'Price Alert! {product.get_model()} {product.get_price()}.' 
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    
    message = service.users().messages().send(userId = 'me', body={'raw' : raw_string}).execute()
    if message['labelIds'][0] == 'SENT':
        return True
    return False

def check_gmail_server():
    if not os.path.exists("client.json"):
        print("Please provide client.json")
        return False
    if not os.path.exists("email.txt"):
        print("Please provide email.txt")
        return False
    with open("email.txt", "r") as f:
        file = f.readlines()
        email_ = file[0].strip()
    CLIENT_FILE = 'client.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)