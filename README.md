# Project-Wizard

Project-Wizard is a python script created to initialize the files and directories for dockerized Django and React fullstack web project according the following structure:
```
project
│    docker-compose.test.yml
│    docker-compose.staging.yml
│    docker-compose.prod.yml
|
└─── Frontend
│    └─── App1
|    |    |    [React project files..]
|    |    |    dockerfile.test
|    |    |    dockerfile.staging
|    |    |    dockerfile.prod
│    └─── App2
|    |    |    [React project files..]
|    |    |    dockerfile.test
│    │    ...
|
└─── Backend
|    │    [Django project files..]
|    |    |    dockerfile.test
|
└─── .env
     |    app1.test.env
     |    app1.staging.env
     |    app1.prod.env
     |    app2.test.env
     |    ...
     |    backend.test.env
     |    ...
```

## Installation

Download and extract the .zip file or clone the repository
```bash
git clone https://github.com/DeXtreme/project-wizard.git
```

## Usage

To create a project with a specific name:
```bash
python wizard.py -p project-name ./path/to/ app1 [app2 app3 ...] 
```

To create a project by first cloning a repository:
```bash
python wizard.py -g https://github.com/usethis/repo.git ./to/path/ app1 [app2 app3 ...] 
```

## Future Additions

* Add support for other frontend and backend frameworks
* Include general parameters and code to the .env, dockerfiles and docker-compose files
* Include a .env folder and docker-compose files in each app and the backend and combine them in the main docker-compose files


## Contributing
Comments, suggestions, ideas and pull requests are welcome.  For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
