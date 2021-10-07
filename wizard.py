import argparse
import os
import subprocess
from pathlib import Path
from distutils import dir_util

class Wizard:
    def __init__(self,
                 project_dir,
                 frontends,
                 project_name = None,
                 git_repo = None,
                 backend = "api") -> None:
        """Initializes project files and directories
        
        Parameters
        ----------

        project_dir : str
            The path to create the project directory at
        frontends : [str, ...]
            A list of the names of the frontend projects
        project_name : str
            The name of the project directory. If omitted the name of
            github repo will be used instead
        git_repo: str
            The URL of the github repo to be cloned
        backend : str
            The name of the backend project

        """

        self.project_dir = project_dir
        self.project_name = project_name
        self.git_repo = git_repo
        self.frontends = frontends
        self.backend = backend
        os.chdir(self.project_dir)

    def clone_git(self):
        # Clone the git repo
        print(f"==== Cloning {self.git_repo} repository ====")
        subprocess.run(["git", "clone", self.git_repo], check=True)
        self.project_name = self.git_repo.split("/")[-1]

    def create_project(self):
        # Create the project folder
        print(f"==== Creating {self.project_name} project folder ====")
        dir_util.mkpath(self.project_name)

    def create_main_dir(self):
        # Create the frontend and backend subdirectories
        print("==== Creating main directories ====")
        dir_util.mkpath(f"./{self.project_name}/Frontend")
        dir_util.mkpath(f"./{self.project_name}/Backend")
    
    def create_dockerfiles(self, path):
        # Create test,staging and production dockerfiles at `path`
        Path(f"{path}/dockerfile.test").touch()
        Path(f"{path}/dockerfile.staging").touch()
        Path(f"{path}/dockerfile.prod").touch()
    
    def create_env_files(self, name):
        # Create .env files
        Path(f"./{self.project_name}/.env/{name}.test.env").touch()
        Path(f"./{self.project_name}/.env/{name}.staging.env").touch()
        Path(f"./{self.project_name}/.env/{name}.prod.env").touch()

    def create_frontends(self):
        #Create frontend webapps
        print("==== Creating frontends ====")
        subprocess.run(f"npx create-react-app ./{self.project_name}/Frontend/tmp", check=True, shell=True)
        for app in self.frontends:
            print(f".... Creating {app} app ....")
            dir_util.copy_tree(f"./{self.project_name}/Frontend/tmp", f"./{self.project_name}/Frontend/{app}")
            self.create_dockerfiles(f"./{self.project_name}/Frontend/{app}")
            
        dir_util.remove_tree(f"./{self.project_name}/Frontend/tmp")     

    
    def create_backend(self):
        #Create backend with a docker container
        print(f"==== Creating {self.backend} backend ====")
        cwd = os.getcwd()
        subprocess.run(["docker", "run", "--rm", "-v", 
                        f"{cwd}/{self.project_name}/Backend:/api",
                        "python:3.7-alpine", 
                        "sh", "-c", 
                        f"pip install django;cd /api;django-admin startproject {self.backend} ."],check=True)
        
        self.create_dockerfiles(f"./{self.project_name}/Backend")

    def create_env(self):
        # Create .env folder and files
        print("==== Creating .env folder ====")
        dir_util.mkpath(f"./{self.project_name}/.env")
        for app in self.frontends:
            print(f".... Creating {app} app .env files ....")
            self.create_env_files(app)
        
        print(f".... Creating {self.backend} .env files ....")
        self.create_env_files(self.backend)
    
    def create_docker_compose_files(self):
        # Create docker compose file
        print("==== Creating docker-compose files ====")
        Path(f"./{self.project_name}/docker-compose.test.yml").touch()
        Path(f"./{self.project_name}/docker-compose.staging.yml").touch()
        Path(f"./{self.project_name}/docker-compose.prod.yml").touch()

    def __call__(self):
        try:
            if self.project_name:
                self.create_project()
            else:
                self.clone_git()
        
            self.create_main_dir()
            #self.create_frontends()
            self.create_backend()
            self.create_env()
            self.create_docker_compose_files()

            print("#*#* HAPPY CODING *#*#")
        except Exception as error:
            print(error)


parser = argparse.ArgumentParser(description="Initializes fullstack web project files and directories")
parser.add_argument("path", nargs="?", default="./", help="Project path")
parser.add_argument('apps', nargs="+", help="Frontend project names")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-p","--project", help="Project name")
group.add_argument("-g","--git", help="GitHub repository")
parser.add_argument("-b","--api", default="api", help="Backend project name")

args = parser.parse_args()

instance = Wizard(args.path, 
                  args.apps,
                  args.project,
                  args.git,
                  args.api)

instance()
