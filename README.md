## API for [APM-APP](https://github.com/Abled-Taha/apm-app) & [APM-APP-WEB](https://github.com/Abled-Taha/apm-app-web)

# Pre-requisites
1. [Downloading & Installing](https://medium.com/@LondonAppBrewery/how-to-download-install-mongodb-on-windows-4ee4b3493514) [MongoDB](https://mongodb.com)
2. [Setting up the Admin User](https://www.mongodb.com/docs/manual/tutorial/configure-scram-client-authentication/)
3. [Downloading & Installing](https://www.geeksforgeeks.org/how-to-install-python-on-windows/) [Python](https://python.org)

# Setting up APM-API
1. [Create a database](https://www.w3schools.com/mongodb/mongodb_mongosh_create_database.php) named "apm"
2. [Create a user with access of reading and writing to the database](https://www.geeksforgeeks.org/create-user-and-add-role-in-mongodb/)
3. Clone the repository
4. Open a terminal in "./apm-server"
5. Run ```pip install -r ./requirements.txt```
6. Run ```cd ./api```
7. Run ```python manage.py collectstatic```
8. Run ```cd ..```
9. Run ```python main.py```
10. Open http://127.0.0.1:8080/docs and follow the recommendations there to securely setup the API
11. Restart the API

### Todo
1. Add ability to change user credentials
2. Find a better way to encrypt passwords without using master password hash