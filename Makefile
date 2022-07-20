run-flask:
	python app.py

run:
	gunicorn -c gunicorn_config.py app:app