run:
	streamlit run main.py
docker-compose:
	docker compose -f docker-compose.yml up -d --build --remove-orphans
docker-run:
	docker run -d -p 8501:8501 --name teste-tecnico app
docker-down:
	docker compose down