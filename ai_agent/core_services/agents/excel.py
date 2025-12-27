from .base import AgentBase
from typing import Dict, Any, List, Optional
import os
from O365 import Account
from ai_agent.profiles.models import O365Token
import datetime
import pandas as pd
import tempfile
from asgiref.sync import sync_to_async
from ai_agent.core_services.models import Agent
import openai

try:
    import openpyxl  # noqa: F401
    OPENPYXL_AVAILABLE = True
except Exception:
    OPENPYXL_AVAILABLE = False

class ExcelAgent(AgentBase):
    def __init__(self, agent_instance: Agent, user=None, file_path=None, **kwargs):
        super().__init__(agent_instance)
        self.user = user
        self.file_path = file_path
        self.account = None
        self.client = kwargs.get('client') or openai.OpenAI()

    async def _ensure_account(self):
        if self.account is not None and self.account.is_authenticated:
            return
        if not self.user or not getattr(self.user, 'is_authenticated', False):
            self.account = None
            return
        try:
            token_data = await sync_to_async(O365Token.objects.get)(user=self.user)
            if token_data.token_expiry > datetime.datetime.now(datetime.timezone.utc):
                credentials = (os.getenv("MS_CLIENT_ID"), os.getenv("MS_CLIENT_SECRET"))
                token = {
                    'access_token': token_data.access_token,
                    'refresh_token': token_data.refresh_token,
                    'expires_at': token_data.token_expiry.timestamp()
                }
                self.account = Account(credentials, auth_flow_type='authorization', token=token)
        except O365Token.DoesNotExist:
            self.account = None

    def _read_dataframe(self, path: str) -> pd.DataFrame:
        lower = path.lower()
        if lower.endswith('.csv'):
            return pd.read_csv(path)
        if lower.endswith('.tsv') or lower.endswith('.tab'):
            return pd.read_csv(path, sep='\t')
        if lower.endswith('.json'):
            return pd.read_json(path)
        if lower.endswith('.xlsx'):
            if not OPENPYXL_AVAILABLE:
                raise RuntimeError("Missing dependency: openpyxl is required to read .xlsx files. Please install openpyxl.")
            return pd.read_excel(path, engine='openpyxl')
        if lower.endswith('.xls'):
            try:
                return pd.read_excel(path)
            except Exception as e:
                raise RuntimeError(f"Unable to read .xls file. Install xlrd (older) or convert to .xlsx. Details: {e}")
        return pd.read_csv(path)

    def _df_context(self, df: pd.DataFrame, max_rows: int = 5) -> str:
        sample = df.head(max_rows)
        describe = None
        try:
            describe = df.describe(include='all').to_string()
        except Exception:
            describe = ""
        context_parts = [
            f"Columns: {list(df.columns)}",
            f"Shape: {df.shape}",
            f"Head:\n{sample.to_string()}",
            f"Describe:\n{describe}" if describe else ""
        ]
        return "\n\n".join([p for p in context_parts if p])

    def _count_users(self, df: pd.DataFrame) -> int:
        cols_lower = {c.lower(): c for c in df.columns}
        if 'email' in cols_lower:
            col = cols_lower['email']
            return int(df[col].dropna().nunique())
        first = cols_lower.get('first name') or cols_lower.get('firstname') or cols_lower.get('first')
        last = cols_lower.get('last name') or cols_lower.get('lastname') or cols_lower.get('last')
        if first and last:
            return int(df[[first, last]].dropna().drop_duplicates().shape[0])
        try:
            if df.shape[1] <= 3:
                return int(df.dropna().drop_duplicates().shape[0])
        except Exception:
            pass
        return int(df.shape[0])

    async def _llm_answer(self, question: str, df: pd.DataFrame) -> Optional[str]:
        if not self.client:
            return None
        try:
            context = self._df_context(df)
            system = (
                "You are a helpful data analyst. You will be given a short context with table columns, "
                "shape, a sample of rows, and statistical description. Answer the user's question strictly "
                "based on this context. If the answer is ambiguous, state assumptions succinctly. Keep the answer concise."
            )
            user_msg = f"Context (from uploaded file):\n\n{context}\n\nQuestion: {question}"
            response = self.client.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.2,
                max_tokens=400,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return None

    async def _process_local_file(self, prompt: str) -> Dict[str, Any]:
        try:
            df = self._read_dataframe(self.file_path)

            prompt_lower = prompt.lower()
            if "convert to xlsx" in prompt_lower or "to xlsx" in prompt_lower:
                with tempfile.NamedTemporaryFile(prefix="converted_", suffix=".xlsx", delete=False, dir=os.path.dirname(self.file_path)) as tmp:
                    out_path = tmp.name
                try:
                    df.to_excel(out_path, index=False)
                    return {"result": f"ExcelAgent: Converted file saved to {out_path}."}
                except Exception as e:
                    return {"error": f"ExcelAgent: Conversion failed: {e}"}

            if "summarize" in prompt_lower or "summarise" in prompt_lower or "summary" in prompt_lower:
                llm = await self._llm_answer("Provide a brief, bullet-point summary of this dataset.", df)
                if llm:
                    return {"result": f"ExcelAgent (summary):\n{llm}"}
                return {"result": f"ExcelAgent: Columns {list(df.columns)} | Rows {len(df)}"}

            if ("how many" in prompt_lower and ("user" in prompt_lower or "people" in prompt_lower or "rows" in prompt_lower)) or ("count" in prompt_lower and "user" in prompt_lower):
                count = self._count_users(df)
                return {"result": f"ExcelAgent: Estimated number of users: {count}"}

            if "describe" in prompt_lower:
                return {"result": f"ExcelAgent: Here is a description of the data:\n{df.describe(include='all').to_string()}"}
            if "head" in prompt_lower or "preview" in prompt_lower:
                return {"result": f"ExcelAgent: Here are the first 5 rows of the data:\n{df.head().to_string()}"}
            if "columns" in prompt_lower or "schema" in prompt_lower:
                return {"result": f"ExcelAgent: Columns detected: {list(df.columns)}"}
            if "rows" in prompt_lower or "count" in prompt_lower:
                return {"result": f"ExcelAgent: Row count: {len(df)}"}

            llm_answer = await self._llm_answer(prompt, df)
            if llm_answer:
                return {"result": f"ExcelAgent: {llm_answer}"}

            return {"result": "ExcelAgent: I have loaded the file. You can ask me to 'describe', show the 'head', list 'columns', 'rows' count, 'convert to xlsx', or ask questions in natural language (requires OPENAI_API_KEY)."}
        except Exception as e:
            return {"error": f"ExcelAgent: Error processing file: {e}"}

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        if self.file_path:
            return await self._process_local_file(prompt)

        await self._ensure_account()
        if not self.account or not self.account.is_authenticated:
            return {"result": "ExcelAgent: Please authenticate with Microsoft to use Excel features. You can do so by visiting /ms_auth/login"}

        if "onedrive" in prompt.lower() or "files" in prompt.lower():
            storage = self.account.storage()
            my_drive = storage.get_default_drive()
            root_folder = my_drive.get_root_folder()
            files = await sync_to_async(root_folder.get_items)()
            file_list = [item.name for item in files]
            return {"result": f"ExcelAgent: Here are some of your files in OneDrive: {file_list}"}

        return {"result": "ExcelAgent: I am connected to your Microsoft account. What would you like to do with Excel?"}


    def get_capabilities(self) -> List[str]:
        return ["read_files_from_onedrive", "create_excel_file", "process_uploaded_file"]

