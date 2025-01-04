
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
load_dotenv()
import os
SECRET_KEY = os.getenv("OPENAI_KEY")


db = SQLDatabase.from_uri('')

print(db.dialect)
print(db.get_usable_table_names())


llm = ChatOpenAI(
    openai_api_key="",
    model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
agent_executor.invoke(
    "using the UserData table, find the owner name of vehicle having vehiclenumber TN 23 ZG 4875"
)