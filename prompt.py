sql = """{
  "instruction": "You are an expert in SQL query generation. Given a natural language question, generate a valid SQL query based on the following database schema.",
  "requirements": [
    "Account for the case sensitivity of column names in PostgreSQL. If the column names in the schema are written in a mixed case (e.g., \"Client_Region\"), they should be enclosed in double quotes. If the column names are lowercase (e.g., client_region), use lowercase letters without quotes.",
    "Always ensure that the query is valid for PostgreSQL by using the correct column and table names."
  ],
  "database_schema": {
    "table_name": "freelancers",
    "columns": {
      "Freelancer_ID": "INT",
      "Job_Category": "VARCHAR",
      "Platform": "VARCHAR",
      "Experience_Level": "VARCHAR",
      "Client_Region": "VARCHAR",
      "Payment_Method": "VARCHAR",
      "Job_Completed": "INT",
      "Earnings_USD": "NUMERIC(10,2)",
      "Hourly_Rate": "NUMERIC(10,2)",
      "Job_Success_Rate": "NUMERIC(5,2)",
      "Client_Rating": "NUMERIC(3,2)",
      "Job_Duration_Days": "INT",
      "Project_Type": "VARCHAR",
      "Rehire_Rate": "NUMERIC(5,2)",
      "Marketing_Spend": "NUMERIC(10,2)"
    }
  },
  "examples": [
    {
      "question": "What is the average earnings of freelancers?",
      "query": "SELECT AVG(\"Earnings_USD\") FROM freelancers;"
    },
    {
      "question": "What are the job categories?",
      "query": "SELECT \"Job_Category\" FROM freelancers;"
    }
  ]
}
"""
protector = """
{
  "instruction": "You are an PostgreSQL validation expert. Your task is to analyze the provided SQL query based on the following criteria:",
  "criteria": [
    "The query must be a valid SQL statement.",
    "The query must only contain `SELECT` statements.",
    "The query must reference only existing columns in the `freelancers` table.",
    "No modifications (`INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.) are allowed."
  ],
  "database_schema": {
    "table_name": "freelancers",
    "columns": {
      "Freelancer_ID": "INT",
      "Job_Category": "VARCHAR",
      "Platform": "VARCHAR",
      "Experience_Level": "VARCHAR",
      "Client_Region": "VARCHAR",
      "Payment_Method": "VARCHAR",
      "Job_Completed": "INT",
      "Earnings_USD": "NUMERIC(10,2)",
      "Hourly_Rate": "NUMERIC(10,2)",
      "Job_Success_Rate": "NUMERIC(5,2)",
      "Client_Rating": "NUMERIC(3,2)",
      "Job_Duration_Days": "INT",
      "Project_Type": "VARCHAR",
      "Rehire_Rate": "NUMERIC(5,2)",
      "Marketing_Spend": "NUMERIC(10,2)"
    }
  },
  "response_if_safe": {
    "answer": "safe"
  },
  "examples": [
    {
      "provided_sql_query": "SELECT Client_Region, Job_Completed FROM freelancers WHERE Job_Success_Rate < 50;",
      "expected_result": {
        "answer": "safe"
      }
    },
    {
      "provided_sql_query": "INSERT INTO freelancers (Freelancer_ID, Job_Category) VALUES (1, 'Developer');",
      "expected_result": {
        "answer": "unsafe"
      }
    }]
}

"""

text = """
{
  "prompt": "User asked: {question}, your assistants generated a database query {sql_data}, verified {protector_data}, and received the response {df} or {error}. You need to respond briefly to the user who asked the question."
}
"""