# Timer-Function-V2-SQL-Read-Write-LLM-Call
This is to demonstrate how we can run an Azure Function V2 every minute based on a Timer Trigger. This function gets a batch of rows from a SQL DB table, makes a gpt-4o call for each row to build a marketing statement and save it in another table. With batich size of 5, based on this query, we see the distribution of batch run time (Batch_run_time.png). The avarage is 8 seconds.
~~~
traces | where message contains "Succeeded"
| project timestamp, second = datetime_part("second", timestamp)
~~~

To develop this function on you PC, you need the latest Azure Function SDK (Core Tool) installed from 
[here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python)

To run this in your Azure subscription, you need the followings:
- Azure Function
- Azure Storage Account
- Azure SQL Server created with a database prepopulated with the SalesLT data
- Azure AI Service with a gpt-4o deployed

Since we are using SQL user authentication so make sure it is enabled (see picture db_auth.png for details). Since we are using shared key for blob access, make sure it is enabled (see picture blob_ky.png).

You also need to create a new table under schema SalesLT with SQL script create.sql.


