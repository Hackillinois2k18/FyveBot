clean:
	rm -r *.pyc
run:
	python manage.py runserver
build:
	pip install -r requirements.txt

help:
	@echo "    clean"
	#echo "	   run"
