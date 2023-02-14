import json
import os
import shutil
import string
import subprocess
from re import sub


class StagedCdkProject:
    def __init__(self, name, path, config='config/example.json'):
        self.name = name
        self.path = path
        self.config = config

        self.project_name = name
        self.camel_case_name = ""
        self.entrypoint = "cdk.ts"
        self.workdir = self.path + "/" + self.name
        self.project_stages = [{}]

        self.setup()

        self.create_base_cdk_project()

        self.update_entry_point()

        self.setup_src_directory()

        self.generate_stages()

        self.run_install()

    def setup(self):
        try:
            os.mkdir(self.workdir)
        except OSError as error:
            print(error)
        with open(self.config, "r") as f:
            self.project_stages = json.load(f)

    def create_base_cdk_project(self):
        cdk_project = subprocess.Popen(["cdk", "init", "app", "--language=typescript"], cwd=self.workdir)
        cdk_project.wait()

    def update_entry_point(self):
        with open(self.workdir+"/package.json", "r") as f:
            project = json.load(f)
            self.project_name = project['name']
        self.entrypoint = self.workdir+"/bin/"+self.project_name + '.ts'
        self.camel_case_name = camel_case(self.project_name)
        print(self.camel_case_name)
        shutil.copy('templates/cdk.ts.template', self.entrypoint)

    def setup_src_directory(self):
        print("Setup src")
        shutil.rmtree(self.workdir+"/lib")
        shutil.copytree("templates/src-dir-template", self.workdir+"/src")

    def generate_stages(self):
        print("generateStages")
        regions = []
        for item in self.project_stages:
            for ou in item:
                for account in item[ou]:
                    for region in item[ou][account]:
                        print(region)
                        regions+=region
                        self.create_stage(ou, account, region)

    def create_stage(self, ou, account, region):
        os.makedirs(self.workdir + "/src/stages/" + ou + "/" + account + "/" + region)
        self.create_ou(ou)
        self.create_account(ou, account)

    def create_ou(self, ou):
        with open("templates/ou.template") as t:
            template = string.Template(t.read())
        ou_index = template.substitute(ou=ou, ou_camel_case=camel_case(ou))
        with open(self.workdir+"/src/stages/"+ou+"/index.ts", "w") as output:
            output.write(ou_index)

    def create_account(self, ou, account):
        with open("templates/account.template") as t:
            template = string.Template(t.read())
        account_index = template.substitute(ou=camel_case(ou), account=account, class_name=camel_case(ou) + camel_case(account))
        with open(self.workdir + "/src/stages/" + ou + "/" + account + "/index.ts", "w") as output:
            output.write(account_index)

    def run_install(self):
        print("run install")
        install = subprocess.Popen(["npm", "install"], cwd=self.workdir)
        install.wait()

def camel_case(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return ''.join(string)


def main():
    path = "/home/todd/clients/rbn/cdk-workspace/test-projects"
    name = "AwesomeByPython"

    project = StagedCdkProject(name, path)


if __name__ == "__main__":
    main()