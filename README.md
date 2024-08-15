# OnlyShop
This is a web store created with Django, Python, HTML, CSS and Bootstrap

### Run the project on web address: https://onlyshop.onrender.com/
- Note that the project is hosted on a free server and may take some (2-3 minutes) time to load

### Run locally:
- Install PostgresSQL
- Install Python
- Optional IDE - install PyCharm so that you can easily run the project
- Create a virtual environment in the terminal with the command `python -m venv venv`
- In the terminal run the command `pip install -r requirements.txt`
- Then create a database in PostgresSQL
- In the terminal run the command `python manage.py migrate` so that the database is created and set
- Then in the terminal run `python manage.py runserver` and open the link in the browser

### Here you can:
- Register, Log In, Edit, Delete, View users
- Create, Edit, Delete, View items
- Filter items by name and category
- Add or remove items from shopping bag
- Create shopping orders

### Easy insert test data:
- Open https://www.mockaroo.com/
- Populate database like this:
![img.png](screenshots/mockaroo.jpg)

### Screenshots:
![img.png](screenshots/img.png)
![img.png](screenshots/user.png)
![img.png](screenshots/cart.png)
