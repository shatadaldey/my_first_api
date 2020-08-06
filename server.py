# Import libraries
import os
import flask 
from flask import request
from google.cloud import bigquery
import matplotlib.pyplot as plot


# Initialize flask application
app_flask = flask.Flask(__name__, 
	static_url_path="/", 
	static_folder="./interface")


# Define API route
@app_flask.route("/")
def root():
	return app_flask.send_static_file("index.html")


@app_flask.route("/year")
def fetch_story_details(methods=['GET']):

	# Fetch query parameter
	query_params = request.args
	year = query_params["year"]

	# Fetch details from DB
	# 1. Establish credentials
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/shatadaldey/Desktop/pandas/my_key.json"

	# 2. Establish BQ client
	client = bigquery.Client()

	# 3. Query
	sql_query = """
		SELECT 
			{year} as year,
			A.year_{year}/1000000 as population
			
		FROM 
			`deft-effect-282902.population.population_by_country` as A
		WHERE 
			A.country = "World"
	"""

	# 4. Fetch results
	result = list(client.query(sql_query.format(year = year)))
	# print(result)


	# Return response to 
	return "The population (in Million) for the year {} is/was : {}".format(result[0]['year'], 
		result[0]['population']), 200



app_flask.run(port=8002, host='0.0.0.0')
