# API / Server for [APM-APP](https://github.com/Abled-Taha/apm-app)

## Setup MongoDB
###### MongoDB must have been installed already and the root user must have setup already.
###### All the credentials can be changed but need to be edited in this Project's `config.json` file to be matched.
1) Login with root user.
2) Make DB `use apm`
3) Make collection `db.createCollection("users")`
4) Make collection `db.createCollection("users-data")`
5) Make user `db.createUser({user:"apm",pwd:passwordPrompt(),roles:[{role:"readWrite",db:"apm"}]})`
6) The password can be set to anything but the same password must be set in this Project's `config.json` file.

## Clone & Run Project
###### Must have Python, MongoDB and Docker/Docker-Compose installed and setup already.
1) Clone this Repository `git clone https://github.com/Abled-Taha/apm-server`
2) Open Terminal in the cloned directory.
3) Run container `docker-compose up` If on Linux, run with `sudo` If made changes to any file then `docker-compose up --build`

###### The port on which the server runs on is recommended to not be changed but could be changed. Firstly should be changed in `nginx.conf` file 
```
http {
  server {
    listen <Desired Port>;

    location / {
      proxy_pass http://app:5001;
    }
  }
}
```
###### then should be changed in
```
  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    ports:
      - "<Desired Port>:<Desired Port>"
```
###### Anything other than the marked ports must not be touched unless you know your own way.