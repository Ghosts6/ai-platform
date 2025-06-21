import os
from O365 import Account, FileSystemTokenBackend
from dotenv import load_dotenv
load_dotenv()

credentials = (os.getenv("MS_CLIENT_ID"), os.getenv("MS_CLIENT_SECRET"))
print("CLIENT_ID:", credentials[0])
print("CLIENT_SECRET:", credentials[1])
print("TENANT_ID:", os.getenv("MS_TENANT_ID"))
print("CLIENT_ID length:", len(credentials[0]) if credentials[0] else 0)
print("CLIENT_SECRET length:", len(credentials[1]) if credentials[1] else 0)
print("TENANT_ID length:", len(os.getenv('MS_TENANT_ID')) if os.getenv('MS_TENANT_ID') else 0)

token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')
try:
    account = Account(credentials, token_backend=token_backend, tenant_id=os.getenv("MS_TENANT_ID"))
    if not account.is_authenticated:
        print("Authenticating with minimal scope...")
        account.authenticate(scopes=['offline_access'], auth_flow_type='device')
    else:
        print("Already authenticated!")
except Exception as e:
    print("Exception during authentication:", e)