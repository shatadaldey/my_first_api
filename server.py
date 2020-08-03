# Import libraries
import os
import flask 
from flask import request
from google.cloud import bigquery


# Initialize flask application
app_flask = flask.Flask(__name__, 
	static_url_path="/", 
	static_folder="./interface")


# Define API route
@app_flask.route("/")
def root():
	return app_flask.send_static_file("index.html")


@app_flask.route("/story-details")
def fetch_story_details(methods=['GET']):

	# Fetch query parameter
	query_params = request.args
	story_id = query_params["storyid"]

	# Fetch details from DB
	# 1. Establish credentials
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "provide-path-to-service-account-credentials.json"

	# 2. Establish BQ client
	client = bigquery.Client()

	# 3. Query
	sql_query = """
		SELECT 
			A.id, 
			A.by, 
			A.score, 
			A.title 
		FROM 
			`dev-mantarays.HACKERNEWS.stories` as A
		WHERE 
			A.id = {story_id}
	"""

	# 4. Fetch results
	result = list(client.query(sql_query.format(story_id = story_id)))
	print(result)

	# Return response to 
	return "Story Id: {}, Published by: {}, Score: {}, Title: {}".format(result[0]['id'], 
		result[0]['by'], result[0]['score'], result[0]['title']), 200


app_flask.run(port=8000, host='0.0.0.0')
