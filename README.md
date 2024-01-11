# API / Server for [APM-APP](https://github.com/Abled-Taha/apm-app)

## Setup MongoDB

###### MongoDB must have been installed already and the root user must have setup already.

###### All the credentials can be changed but need to be edited in this Project's `config.json` file to be matched.

1. Login with root user.
2. Make DB `use apm`
3. Make collection `db.createCollection("users")`
4. Make collection `db.createCollection("users-data")`
5. Make user 
  ```
  db.createUser(
    {
      user:"apm",
      pwd:passwordPrompt(),
      roles:[
        {
          role:"readWrite",
          db:"apm"
        }
      ]
    }
  )
  ```
6. The password can be set to anything but the same password must be set in this Project's `config.json` file.

## Clone & Run Project

###### Must have Python and MongoDB installed and setup already.

1. Clone this Repository `git clone https://github.com/Abled-Taha/apm-server`
2. Open Terminal in the cloned directory.
3. Install Dependencies `pip install -r requirements.txt`
4. Modify the `config/config.json` file to have correct credentials.
5. Change directory `cd api`
6. Collect Static Files `python manage.py collectstatic`
7. Do Migration `python manage.py migrate`
8. This is the Final and the only step which needs to be repeated if running the server again after stopping it. Run server by `python manage.py runserver`


## Documentation

###### To visit the documentation, visit the `docs/` page on the API.