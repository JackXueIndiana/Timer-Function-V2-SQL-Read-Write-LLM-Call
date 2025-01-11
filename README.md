# Timer-Function-V2-SQL-Read-Write-LLM-Call
This is to demonstrate how we can run an Azure Function V2 every minute based on a Timer Trigger. This function gets a row from a SQL DB table, makes a gpt-4o call to build a marketing statement and save it in another table. All these steps can be accomplished in 6 seconds. 

To develop this function on you PC, you need the latest Azure Function SDK (Core Tool) installed from 
[here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python)

To run this in your Azure subscription, you need the followings:
- Azure Function
- Azure Storage Account
- Azure SQL Server created with a database prepopulated with the SalesLT data
- Azure AI Service with a gpt-4o deployed

Since we are using SQL user authentication so make sure it is enabled (see picture db_auth.png for details). Since we are using shared key for blob access, make sure it is enabled (see picture blob_ky.png).

You also need to create a new table under schema SalesLT with SQL script create.sql.


