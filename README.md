
**Query Generator Application**

Backend (app.py) Workflow:
1.	Setup Flask Application:
a.	Flask is initialized to serve endpoints for handling schema fetching and query generation.
b.	The CORS library is used to handle cross-origin requests.
2.	Database Schema Retrieval (/fetch_schema):
a.	The /fetch_schema endpoint is called when the webpage loads.
b.	Inside this endpoint:
i.	Connect to the MySQL database using mysql.connector.
ii.	Query the database for the schema using SHOW TABLES and DESCRIBE <table_name> commands.
iii.	Structure the schema as a dictionary containing table names and column details.
iv.	Return the schema as a JSON object.
3.	Query Generation (/generate_query):
a.	The /generate_query endpoint processes user-input actions.
b.	Inside this endpoint:
i.	The user-provided action is received as JSON input.
ii.	A mapping in the generate_query function matches predefined actions to SQL queries.
iii.	The corresponding SQL query is returned in JSON format.
4.	Run Flask Server:
a.	Flask listens for incoming HTTP requests at http://127.0.0.1:5000.

Frontend (index.html) Workflow:
1.	Page Layout:
a.	The page is divided into:
i.	Main Section: Displays the schema, allows input of actions, and shows generated SQL queries.
ii.	Actions Section: Lists predefined actions for users to select.
2.	Fetching Schema:
a.	On page load, a JavaScript function makes an HTTP GET request to the /fetch_schema endpoint.
b.	The fetched schema is displayed in the "Schema" section.
3.	Generating Queries:
a.	User can:
i.	Manually Enter Actions:
1.	Input a natural-language action into the text box.
2.	Click "Generate Query" to send the input to /generate_query via a POST request.
3.	Display the returned SQL query in the "Generated SQL Query" section.
ii.	Use Suggested Actions:
1.	Click on a predefined action from the right-side "Suggested Actions" section.
2.	Automatically fills the action input field.
3.	Triggers the /generate_query endpoint to fetch and display the corresponding query.
4.	JavaScript Functions:
a.	fetchSchema():
i.	Sends a request to fetch the schema and displays it.
b.	generateQuery(action):
i.	Sends the action to /generate_query.
ii.	Displays the returned SQL query in the UI.
c.	selectAction(actionText):
i.	Fills the input field with the selected action and calls generateQuery.

Execution Flow:
1.	User Visits the Application:
a.	The schema is loaded and displayed.
b.	Suggested actions are visible in the "Suggested Actions" section.
2.	User Inputs or Selects an Action:
a.	The action is sent to the Flask backend via the /generate_query endpoint.
3.	Backend Processes the Action:
a.	Matches the action with a predefined SQL query in the generate_query function.
b.	Returns the SQL query to the frontend.
4.	Query Displayed:
a.	The generated query is shown in the "Generated SQL Query" section.

 

 
