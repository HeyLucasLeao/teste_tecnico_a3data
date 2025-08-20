.PHONY: run
run:
	streamlit run main.py

docker-build:
	docker-compose up --build 

docker-run:
	docker run -d -p 8501:8501 --name teste-tecnico app
