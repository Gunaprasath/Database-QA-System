import google.generativeai as genai
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import Runnable
from few_shots import few_shots  # Import the few-shot examples

import mysql.connector
from mysql.connector import connection, Error
from urllib.parse import quote_plus
import re
import time


# Function to convert a tuple to a string
def tuple_to_string(input_tuple):
    """Convert a tuple to a single string."""
    if isinstance(input_tuple, tuple):
        return ' '.join(str(x) for x in input_tuple)
    return str(input_tuple)


# GenAIRunnable class to integrate GenAI with LangChain
class GenAIRunnable(Runnable):
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)

    def _call(self, inputs: str, **kwargs) -> str:
        """Call GenAI and return the output."""
        inputs = tuple_to_string(inputs)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(inputs)
        output = response.text

        # Handle stop tokens if provided
        stop = kwargs.get("stop", None)
        if stop:
            for token in stop:
                if token in output:
                    output = output.split(token)[0]
                    break
        return output

    def invoke(self, inputs: str, config=None, **kwargs) -> str:
        """Invoke the _call method."""
        return self._call(inputs, **kwargs)


# Function to set up the SQLDatabaseChain
def get_few_shot_db_chain():
    db_user = "root"
    db_password = quote_plus("#Guna@80")
    db_host = "localhost"
    db_name = "new_db"

    db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"
    db = SQLDatabase.from_uri(db_url, sample_rows_in_table_info=3)

    # Include few-shots in the prompt
    sql_prompt = PromptTemplate(
        input_variables=["question", "db_tables_info", "few_shots"],
        template="""
        You are a MySQL expert. Based on the following schema:
        {db_tables_info}

        Examples:
        {few_shots}

        Now, based on the schema above, answer the question below:
        Question:
        {question}
        SQL Query:
        """
    )

    genai_instance = GenAIRunnable(api_key="AIzaSyBTjmJePmxrYftDwH0cPgMuwA8Lo2F3CbI")
    llm_chain = LLMChain(prompt=sql_prompt, llm=genai_instance)
    return SQLDatabaseChain(database=db, llm_chain=llm_chain, verbose=True)


# Function to clean SQL query
def clean_sql_query(query):
    """Remove markdown and unnecessary comments from the query."""
    query = re.sub(r"```sql|```", "", query)
    query = re.sub(r"--.*", "", query)
    return query.strip()


# Function to execute SQL query
def execute_sql_query(query):
    query = clean_sql_query(query)
    attempt = 0
    max_retries = 3

    while attempt < max_retries:
        try:
            cnx = connection.MySQLConnection(
                host="localhost",
                port="3306",
                database="new_db",
                user="root",
                password="#Guna@80"
            )
            if cnx.is_connected():
                cursor = cnx.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Error as e:
            print(f"Error: {e}")
            attempt += 1
        finally:
            if cnx and cnx.is_connected():
                cursor.close()
                cnx.close()
    return None


def format_result_to_string(result):
    """
    Convert the SQL query result to a string format for consistent output.
    Handles varying structures of the result depending on the query.
    """
    if not result:
        return "No data found."

    # Handle a list of tuples (typical SQL query result)
    if isinstance(result, list):
        return "\n".join(
            [", ".join(map(str, row)) for row in result]
        )

    # Handle a single tuple or value
    if isinstance(result, tuple):
        return ", ".join(map(str, result))

    # Handle other possible return types
    return str(result)


# Function to process user questions
def process_question(question):
    """
    Generate SQL from the question, execute it, and return results as a string.
    """
    try:
        chain = get_few_shot_db_chain()
        db_tables_info = chain.database.get_table_info()

        inputs = {
            "question": question,
            "db_tables_info": db_tables_info,
            "few_shots": few_shots,  # Pass the few_shots examples
        }
        response = chain.llm_chain.invoke(inputs)
        sql_query = response.get("text", "").strip()

        if not sql_query or "SELECT" not in sql_query.upper():
            return "Please ask a question related to the database."

        print(f"Generated SQL Query:\n{sql_query}")  # Debugging
        result = execute_sql_query(sql_query)

        # Convert result to string format
        return format_result_to_string(result)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred. Please try again."
