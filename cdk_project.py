import json
import os
import shutil
import subprocess
import sys

from utils import camel_case
from stage import Stage


class CdkProject:
    def __init__(self, name, workdir, configuration=None):
        self.workdir = workdir
        self.stages = []
        if not configuration:
            self.config = os.path.join(sys.path[0], "config/example.json")
        else:
            self.config = configuration

        self.regions = []

        self.project_name = name
        self.camel_case_name = camel_case(self.project_name)
        self.entrypoint = "cdk.ts"
        self.project_stages = [{}]

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
        with open(self.workdir + "/package.json", "r") as f:
            project = json.load(f)
            self.project_name = project['name']
        self.entrypoint = self.workdir + "/bin/" + self.project_name + '.ts'
        shutil.copy('templates/cdk.ts.template', self.entrypoint)

    def setup_src_directory(self):
        print("Setup src")
        shutil.rmtree(self.workdir + "/lib")
        shutil.copytree("templates/src-dir-template", self.workdir + "/src")

    def generate_stages(self):
        print("Building stages based on the config from " + self.config + ":")
        print(json.dumps(self.project_stages, indent=2))
        print(" ")
        for item in self.project_stages:
            for ou in item:
                for account in item[ou]:
                    for region in item[ou][account]:
                        self.regions.append(region)
                        self.stages.append(Stage(ou, account, region, self.workdir))

    def build(self):
        self.setup()

        self.create_base_cdk_project()

        self.update_entry_point()

        self.setup_src_directory()

        self.generate_stages()
