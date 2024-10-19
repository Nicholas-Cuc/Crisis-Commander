from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from datetime import datetime, timedelta
from supabase import create_client, Client

# Database config
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

print(url)
print(key)

supabase: Client = create_client(url, key)

response = supabase.schema("public").table("feedback").select("*").execute()

print("Response: ", response)


app = Flask(__name__)

"""@app.route('/')
def hello():
    return 'Hello World!'
    """
# # TODO: Login
# # TODO: Log_Out
# # TODO: Add_Faculty
@app.route('/forms', methods=['GET'])
def forms():
    data = supabase.table("forms").select("*").execute()
    return print(data)
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    data = supabase.table("feedback").select("*").execute()
    return print(data)
def get_feedback():
    data = supabase.table("feedback").select("*").execute()
    return data
# # TODO: Add_Patient
# # TODO: View_Patients
# # TODO: View_Faculty
# # TODO: Delete_User
# # TODO: Forms?
# # TODO: Feedback?
# # TODO: IDK

# if __name__ == '__main__':
#     app.run(debug=True)