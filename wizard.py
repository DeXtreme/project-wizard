import argparse
import os
import subprocess
from distutils import dir_util

class Wizard:
    def __init__(self,
                 project_dir,
                 frontends,
                 project_name = None,
                 git_repo = None,
                 backend = "api") -> None:
        """Initializes project files and directories
        
        PARAMETERS
        
        
        """

        self.project_dir = project_dir
        self.project_name = project_name
        self.git_repo = git_repo
        self.frontends = frontends
        self.backend = backend

        os.chdir(self.project_dir)

    def clone_git(self):
        print(f"==== Cloning {self.git_repo} repository ====")
        subprocess.run(["git", "clone", self.git_repo], check=True)
        self.project_name = self.git_repo.split("/")[-1]

    def create_project(self):
        print(f"==== Creating {self.project_name} project folder ====")
        dir_util.mkpath(self.project_name)

    def create_main_dir(self):
        print("==== Creating main directories ====")
        dir_util.mkpath(f"./{self.project_name}/Frontend")
        dir_util.mkpath(f"./{self.project_name}/Backend")

    def create_frontends(self):
        print("==== Creating frontends ====")
        subprocess.run(f"npx create-react-app ./{self.project_name}/Frontend/react")
        for app in self.frontends:
            print(f"==== Creating {app} app ====")
            dir_util.copy_tree(f"./{self.project_name}/Frontend/react", f"./{self.project_name}/Frontend/{app}")
        dir_util.remove_tree(f"./{self.project_name}/Frontend/react")     

    
    def create_backend(self):
        print("==== Creating backend ====")
        

    def create_env(self):
        #make folder
        #add files
        pass

    def __call__(self):
        try:
            if self.project_name:
                self.create_project()
            else:
                self.clone_git()
        
            self.create_main_dir()
            self.create_frontends()
            self.create_backend()
            self.create_env()
        except Exception as e:
            print(e)


parser = argparse.ArgumentParser(description="Initializes fullstack web project files and directories")
parser.add_argument("path", nargs="?", default="./", help="Project path")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-p","--project", help="Project name")
group.add_argument("-g","--git", help="GitHub repository")
parser.add_argument('-f',"--apps", nargs="+", help="Frontend project names")
parser.add_argument("-b","--api", default="api", help="Backend project name")

args = parser.parse_args()

instance = Wizard(args.path, 
                  args.apps,
                  args.project,
                  args.git,
                  args.api)

instance()