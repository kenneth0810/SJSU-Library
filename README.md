# SJSU-Library
A fictional SJSU library web app that simulates RBAC model functionalities, created with Django framework.

## Project Setup
### Clone and cd to the project directory
```
git clone https://github.com/kenneth0810/SJSU-Library.git && cd SJSU-Library
```

### Virtual Environment
1. To create:
```
python3 -m venv .venv
```
2. To activate:
```
source .venv/bin/activate
```
3. Install all necessary packages in venv:
```
pip install -r requirements.txt
```

### Set up Database

1. Run this command first to create necessary tables:
```
python3 manage.py makemigrations sjsu_library && python3 manage.py migrate
```

2a. The data file of trending books is already provided in sjsu_library/fixtures. Run this command to load it into the database:
```
python3 manage.py loaddata trending_books.json
```

2b. Optionally, if you would like to fetch the most recent data, run these commands first before loading the data:
```
python3 data/trending_books.py && cp data/trending_books.json sjsu_library/fixtures/
```

### Running the server
```
python3 manage.py runserver
```
The server will be hosted on http://127.0.0.1:8000/

### Create Admin (optional)
This is to create a user with admin privileges.
```
python3 manage.py createsuperuser
```
The admin page is accessible on http://127.0.0.1:8000/admin

### Project Constraints
- Librarian account credentials are predetermined and hard-coded into the project (email: librarian@sjsu.edu, ID: 123456789) . Do not use those credentials when creating an admin account so that the librarian account can be created and used for the project.
