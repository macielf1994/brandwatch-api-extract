import json
import requests
from bw_requests import BWRequests as bw
from dotenv import load_dotenv
import os
from datetime import datetime

def handler(event, context):
    date_today = datetime.today().strftime('%Y-%m-%d')
    load_dotenv()
    email_brandwatch = os.getenv("EMAIL_BRANDWATCH")
    pass_brandwatch = os.getenv("PASS_BRANDWATCH")
    access_token = bw.get_token(email_brandwatch, pass_brandwatch)
    list_project_ids = bw.get_projects(access_token, [1998281256])
    list_tuples_project_query_id = bw.get_queries(access_token, list_project_ids)
    bw.get_mentions(access_token, list_tuples_project_query_id, '2020-01-01', date_today, 5000)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Lambda Function its working!",
        }),
    }
