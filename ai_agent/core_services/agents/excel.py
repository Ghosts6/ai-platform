from .base import AgentBase
from typing import Dict, Any, List, Optional
import os
from O365 import Account
from profiles.models import O365Token
import datetime
import pandas as pd

class ExcelAgent(AgentBase):
    def __init__(self, agent_id: str, name: str, description: str = "", user=None, file_path=None):
        super().__init__(agent_id, name, description)
        self.user = user
        self.file_path = file_path
        self.account = None
        if self.user and self.user.is_authenticated:
            try:
                token_data = O365Token.objects.get(user=self.user)
                if token_data.token_expiry > datetime.datetime.now(datetime.timezone.utc):
                    credentials = (os.getenv("MS_CLIENT_ID"), os.getenv("MS_CLIENT_SECRET"))
                    token = {
                        'access_token': token_data.access_token,
                        'refresh_token': token_data.refresh_token,
                        'expires_at': token_data.token_expiry.timestamp()
                    }
                    self.account = Account(credentials, auth_flow_type='web', token=token)
            except O365Token.DoesNotExist:
                pass

    async def _process_local_file(self, prompt: str) -> Dict[str, Any]:
        try:
            if self.file_path.endswith('.csv'):
                df = pd.read_csv(self.file_path)
            elif self.file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(self.file_path)
            else:
                return {"result": "ExcelAgent: Unsupported file type. Please upload a CSV or Excel file."}

            # Basic analysis for demonstration
            if "describe" in prompt.lower():
                return {"result": f"ExcelAgent: Here is a description of the data:\n{df.describe().to_string()}"}
            if "head" in prompt.lower():
                return {"result": f"ExcelAgent: Here are the first 5 rows of the data:\n{df.head().to_string()}"}

            return {"result": "ExcelAgent: I have loaded the file. What would you like me to do with it? Ask me to 'describe' the data or show the 'head'."}
        except Exception as e:
            return {"error": f"ExcelAgent: Error processing file: {e}"}

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        if self.file_path:
            return await self._process_local_file(prompt)

        if not self.account or not self.account.is_authenticated:
            return {"result": "ExcelAgent: Please authenticate with Microsoft to use Excel features. You can do so by visiting /ms_auth/login"}

        # Example: Access OneDrive
        if "onedrive" in prompt.lower() or "files" in prompt.lower():
            storage = self.account.storage()
            my_drive = storage.get_default_drive()
            root_folder = my_drive.get_root_folder()
            files = root_folder.get_items()
            file_list = [item.name for item in files]
            return {"result": f"ExcelAgent: Here are some of your files in OneDrive: {file_list}"}

        return {"result": "ExcelAgent: I am connected to your Microsoft account. What would you like to do with Excel?"}


    def get_capabilities(self) -> List[str]:
        return ["read_files_from_onedrive", "create_excel_file", "process_uploaded_file"]

__all__ = ["ExcelAgent"]

