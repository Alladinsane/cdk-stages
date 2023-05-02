import json
import os
import shutil
import subprocess
import sys
import boto3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from .stage import Stage
from .utils import camel_case, create_file


class CdkProject:
    def __init__(self, name, workdir, demo, configuration=None):
        self.workdir = workdir
        self.stages = []
        self.demo = demo

        if not configuration:
            if self.demo:
                print("Using sample template")
                print(os.path.abspath(__file__))
                configuration = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config/example.json")
                print("configuration=" + configuration)

                with open(configuration, 'r') as f:
                    self.project_stages = json.load(f)
            else:
                self.project_stages = []
        else:
            print(configuration)
            with open(configuration, 'r') as f:
                self.project_stages = f.read()

        self.regions = []

        self.project_name = name
        self.camel_case_name = camel_case(self.project_name)
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
        print("Remove default entrypoint")
        os.system(f"rm -rf {self.workdir}/bin/*")
        print("Creating entrypoint")
        with open(self.workdir + "/package.json", "r") as f:
            project = json.load(f)
            self.project_name = project['name']
        self.entrypoint = self.workdir + "/bin/" + self.project_name + '.ts'

        if self.demo:
            comment = ""
        else:
            comment = "// "
        # Edit the entrypoint
        create_file("templates/cdk-ts.template",
                    self.entrypoint,
                    {"comment": comment}
                    )

    def setup_src_directory(self):
        template = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates/src-dir-template")
        print("Setup src")
        shutil.rmtree(self.workdir + "/lib")
        shutil.copytree(template, self.workdir + "/src")

    def create_environment_construct(self):
        if self.demo:
            demo_stack_import = "\nimport { Demo } from '../stacks/demo'"
            demo_stack = '\n\t\tconst app = new Demo(this, "demo-stack", {})\n'
        else:
            demo_stack_import = ""
            demo_stack = ""

        create_file("templates/environment.template",
                    self.workdir + "/src/constructs/environment.ts",
                    {
                        "demo_stack_import": demo_stack_import,
                        "demo_stack": demo_stack}
                    )

    def generate_stages(self):
        print("Building stages:")
        print(json.dumps(self.project_stages, indent=2))
        print(" ")
        DEMO_ACCOUNT_NAME = self.project_stages[0]['accounts'][0]['name']

        for ou in self.project_stages:
            print("ou", ou['name'])
            for account in ou['accounts']:
                if 'account_id' in account:
                    account_connector = f"public static readonly AccountId: string = '{account['account_id']}'"
                else:
                    account_connector = f"public static readonly AccountId: string = '123456789'; // Replace with Account Id for {name}."

                for region in account['regions']:
                    self.regions.append(region)
                    if account['name'] == DEMO_ACCOUNT_NAME and region == 'us-east-1' and self.demo:
                        print(f"Volunteering {DEMO_ACCOUNT_NAME} for demo deployments...")
                        account_connector = f"public static readonly AccountId: string = '{(boto3.client('sts').get_caller_identity().get('Account'))}'"
                    self.stages.append(Stage(ou['name'], account['name'], account_connector, region, self.workdir, self.demo))

    def create_demo_stack(self):
        create_file(
            "templates/demo_stack.template",
            self.workdir + "/src/stacks/demo.ts"
            )

    def create_demo_resource(self):
        create_file(
            "templates/resource.template",
            self.workdir + "/src/resources/sns_topic.ts"
        )

    def build(self):
        self.setup()

        self.create_base_cdk_project()

        self.update_entry_point()

        self.setup_src_directory()

        self.create_environment_construct()

        if self.project_stages:
            self.generate_stages()

        if self.demo:
            self.create_demo_resource()
            self.create_demo_stack()