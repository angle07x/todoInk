# token fetching taken from quickstart.py from https://developers.google.cn/workspace/tasks/quickstart/python?hl=en#1

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/tasks.readonly"]

def authenticate_user(email):
    token_file = f"token_{email}.json"

    creds = None
    # load token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds

def fetch_tasks(email):
    creds = authenticate_user(email)
    service = build("tasks", "v1", credentials=creds)

    # get task lists
    task_lists = service.tasklists().list(maxResults=1).execute()
    items = task_lists.get("items", [])
    if not items: return []

    task_list_id = items[0]["id"]
    tasks_result = service.tasks().list(
        tasklist = task_list_id,
        showHidden = False,
        maxResults = 20
    ).execute()
    tasks = tasks_result.get("items", [])

    
    # fix formatting
    formatted_tasks = []
    for task in tasks:
        if task.get("status") == "needsAction":  # not completed
            formatted_tasks.append({
                "title": task.get("title", ""),
                "priority": "P0" if task.get("title", "").lower().endswith("!") else "P2",
                "done": False
            })
    
    return formatted_tasks

def get_all_users_tasks(all_emails):
    all_tasks = []
    for email in all_emails:
        print("Fetching for ", email)
        tasks = fetch_tasks(email)
        all_tasks.extend(tasks)
    return(all_tasks)
