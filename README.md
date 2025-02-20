## API for [APM-APP](https://github.com/Abled-Taha/apm-app) & [APM-APP-WEB](https://github.com/Abled-Taha/apm-app-web)

# About
The Project [APM-SERVER](https://github.com/Abled-Taha/apm-server), [APM-APP](https://github.com/Abled-Taha/apm-app) & [APM-APP-WEB](https://github.com/Abled-Taha/apm-app-web) are of a larger project known as **APM** which serves to be a Password Manager. None of these repositores or single projects can and should be used just on their own unless stated otherwise. They are meant to be used together.

# Pre-requisites
1. [Downloading & Installing](https://medium.com/@LondonAppBrewery/how-to-download-install-mongodb-on-windows-4ee4b3493514) [MongoDB](https://mongodb.com)
2. [Setting up the Admin User](https://www.mongodb.com/docs/manual/tutorial/configure-scram-client-authentication/)
3. [Downloading & Installing](https://www.geeksforgeeks.org/how-to-install-python-on-windows/) [Python](https://python.org)

# Setting up APM-API
1. [Create a database](https://www.w3schools.com/mongodb/mongodb_mongosh_create_database.php) named "apm"
2. [Create a user with access of reading and writing to the database](https://www.geeksforgeeks.org/create-user-and-add-role-in-mongodb/)
3. Clone the repository
4. Open the directory
5. Make ".env" file
6. Set all the variables in that file from the "config.json" file
7. Open a terminal in "./apm-server"
8. Run ```pip install -r ./requirements.txt ; cd ./api ; python manage.py collectstatic ; cd .. ; python main.py run-server```
9. To generate an api token you can use ```python main.py generate-api-token``` which will be used by client
10. Open http://127.0.0.1:8000/docs and follow the recommendations there to securely setup the API
11. Restart the API

### Todo
1. Add ability to change user credentials
2. Use the .env file for only some credentials.
