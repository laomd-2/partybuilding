1. drop database party;
2. create database party;
3. rm -r $(find . -name migrations) $(find . -name __pycache__)
4. python manage.py makemigrations --empty info user teaching xadmin work notice
5. python manage.py makemigrations
6. python manage.py migrate user
7. python manage.py migrate user
8. python manage.py runserver 0.0.0.0:8000