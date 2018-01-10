1. Please first instantiate PostgreSQL with PostGIS.
(Preferably Docker container of mdillon/postgis)

2. Paste the DB URI in config.json

3. Run models.py
	It will create ORM based tables in the database

### Keep Internet Connected for Step 4 and 5 as it fetches resources from gists ###

4. Run CRUD.py
	It will populate the PinMap table with the csv of First Task

5. Run geoJsonParser.py
	It will populate the FeatureFence with the geojson of the Third Task

6. Run app.py

	1.	/post_location/ <-- Mind the trailing backslash
		expected parameters = ['lat','lon','pin','address','city']
	2.	/get_using_postgres/<float:lat>/<float:lon>/<int:distance>/

	3.	/get_using_self/<float:lat>/<float:lon>/<int:distance>/

	4.	/where_is/<float:lat>/<float:lon>/

7. Response Codes-
	500 - Internal Server Error
	400 - Error in posted data
	404 on GET - Check Parameters ( API won't accept any false URIs )
	200 - OK

	GET responses have 3 attributes -
		{ResponseCode, message, data}

		message = Explains Why ResponseCode
		data = The actual query response

	POST responses have 2 attributes -
		{ResponseCode, message}

		message = Explains Why ResponseCode
