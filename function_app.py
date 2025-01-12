import os
import azure.functions as func
import datetime
import json
import logging
from azure.functions.decorators.core import DataType
from openai import AzureOpenAI

app = func.FunctionApp()

BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("gpt-4o")

@app.function_name(name="TimerSQLLLM")
@app.sql_input(arg_name="productdisc",
    command_text=f'''select Top {BATCH_SIZE} p.ProductID, p.Name, pd.Description from 
[SalesLT].[Product] as p INNER JOIN [SalesLT].[ProductModelProductDescription] as pmpd on p.ProductModelID=pmpd.ProductModelID 
INNER JOIN [SalesLT].[ProductDescription] as pd on pd.ProductDescriptionID = pmpd.ProductDescriptionID
where pmpd.Culture='en' and p.ProductID NOT IN (select ProductID from [SalesLT].[MarketStatement])''',
    command_type="Text",
    connection_string_setting="SqlConnectionString")
@app.sql_output(arg_name="productmarketing",
                        command_text="[SalesLT].[MarketStatement]",
                        connection_string_setting="SqlConnectionString")
@app.timer_trigger(schedule="0 */1 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def TimerSQLLLM(myTimer: func.TimerRequest, 
                productdisc: func.SqlRowList,
                productmarketing: func.Out[func.SqlRow]   
    ) -> None:

    if myTimer.past_due:
        logging.info('The timer is past due at %s', myTimer.schedule_status.last)

    rows = list(map(lambda r: json.loads(r.to_json()), productdisc))
    logging.info('Python timer trigger function executed at %s', datetime.datetime.utcnow())
    logging.info(rows)
    
    for j in rows:
        statement = ""
        llm_error = ""
        query = "Product Name:" + j["Name"] + " Description:" + j["Description"]
        logging.info(f"query: {query}")
        try:
            statement = call_llm(query)
        except Exception as e:
            llm_error = f"LLM error: {e}"  
            logging.error(llm_error)
        finally:
            logging.info(statement)
            j["Statement"] = statement
            j["Status"] = llm_error if llm_error != "" else "Completed"
            del j["Name"]
            del j["Description"]
            
    logging.info(f"DB insert: {rows}")
    sqlRowList = func.SqlRowList(rows)
    productmarketing.set(sqlRowList)

def call_llm(content) -> str:
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-02-01",
    )
    completion = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are an experienced marketing materials writer."},
            {"role": "user", "content": f"Create a compelling marketing statement based on the following text:\n\n{content}"}
        ],
        max_tokens=200, 
        temperature=0.0
    )
    return completion.choices[0].message.content.strip()  