import os
import logging
from O365 import Account, FileSystemTokenBackend
from dotenv import load_dotenv
import time

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

# Use only client ID for device code flow
credentials = os.getenv("MS_CLIENT_ID")
print("CLIENT_ID:", credentials)
print("CLIENT_SECRET:", os.getenv("MS_CLIENT_SECRET"))
print("TENANT_ID:", os.getenv("MS_TENANT_ID"))
print("CLIENT_ID length:", len(credentials) if credentials else 0)
print("CLIENT_SECRET length:", len(os.getenv("MS_CLIENT_SECRET")) if os.getenv("MS_CLIENT_SECRET") else 0)
print("TENANT_ID length:", len(os.getenv('MS_TENANT_ID')) if os.getenv('MS_TENANT_ID') else 0)

# Scopes needed for your app
scopes = [
    'offline_access',
    'User.Read',
    'Calendars.ReadWrite',
    'Mail.ReadWrite',
    'Chat.ReadWrite',
    'Group.ReadWrite.All'
]

token_filename = 'o365_token.txt'

def check_token_file():
    if os.path.exists(token_filename):
        print(f"Token file '{token_filename}' exists!")
    else:
        print(f"Token file '{token_filename}' NOT found!")

print("\nTrying device code flow authentication...")
token_backend = FileSystemTokenBackend(token_path='.', token_filename=token_filename)
try:
    account = Account(credentials, token_backend=token_backend, tenant_id=os.getenv("MS_TENANT_ID"),
                     auth_flow_type='public')
    if not account.is_authenticated:
        print("Authenticating with device code flow and full scopes...")
        account.authenticate(scopes=scopes)
        # Wait a moment for token to be written
        time.sleep(2)
    else:
        print("Already authenticated!")
    check_token_file()
    # Test API access: list calendar events
    try:
        schedule = account.schedule()
        calendar = schedule.get_default_calendar()
        print("Listing up to 3 calendar events:")
        for event in calendar.get_events(limit=3):
            print(f"- {event.subject} | {event.start} - {event.end}")
    except Exception as api_e:
        print(f"API access error: {api_e}")
except Exception as e:
    print(f"Exception during authentication: {e}")
    import traceback
    traceback.print_exc()