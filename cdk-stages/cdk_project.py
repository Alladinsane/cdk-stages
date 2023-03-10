import json
import os
import shutil
import subprocess
import sys

from .stage import Stage
from . import utils


class CdkProject:
    def __init__(self, name, workdir, configuration=None):
        self.workdir = workdir
        self.stages = []

        if not configuration:
            print(os.path.abspath(__file__))
            configuration = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config/example.json")
            print("configuration=" + configuration)

        print(configuration)
        with open(configuration, 'r') as f:
            self.project_stages = f.read()

        self.regions = []

        self.project_name = name
        self.camel_case_name = utils.camel_case(self.project_name)
        self.entrypoint = "cdk.ts"

    def setup(self):
        try:
            os.mkdir(self.workdir)
        except OSError as error:
            print(error)

    def create_base_cdk_project(self):
        cdk_project = subprocess.Popen(["cdk", "init", "app", "--language=typescript"], cwd=self.workdir)
        cdk_project.wait()

    def update_entry_point(self):
        template = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates/cdk-ts.template")
        with open(self.workdir + "/package.json", "r") as f:
            project = json.load(f)
            self.project_name = project['name']
        self.entrypoint = self.workdir + "/bin/" + self.project_name + '.ts'
        shutil.copy(template, self.entrypoint)

        utils.create_file("templates/cdk-ts.template",
                    self.workdir + "/" + self.project_name
        )

    def setup_src_directory(self):
        template = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates/src-dir-template")
        print("Setup src")
        shutil.rmtree(self.workdir + "/lib")
        shutil.copytree(template, self.workdir + "/src")

    def generate_stages(self):
        print("Building stages:")
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
