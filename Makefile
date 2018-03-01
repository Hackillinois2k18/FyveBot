clean:
	find . -name '*.pyc' -delete
run:
	python BotClient.py
build:
	sudo pip install -r requirements.txt

