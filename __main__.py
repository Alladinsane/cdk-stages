import argparse
import json
import os
import shutil
import string
import subprocess
import sys
from re import sub

def create_file(template_path, target_path, params):
    with open(os.path.join(sys.path[0], template_path)) as t:
        template = string.Template(t.read())
    index = template.substitute(**params)
    with open(target_path, "w") as output:
        output.write(index)


def camel_case(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return ''.join(string)


class StagedCdkProject:
    def __init__(self, name, path, configuration=None):
        self.name = name
        self.path = path
        if not configuration:
            self.config = os.path.join(sys.path[0], "config/example.json")
        else:
            self.config = configuration

        self.regions = []

        self.project_name = name
        self.camel_case_name = ""
        self.entrypoint = "cdk.ts"
        self.workdir = self.path + "/" + self.name
        self.project_stages = [{}]

    def build(self):
        self.setup()

        self.create_base_cdk_project()

        self.update_entry_point()

        self.setup_src_directory()

        self.generate_stages()

        self.generate_region_configs()

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
        with open(self.workdir + "/package.json", "r") as f:
            project = json.load(f)
            self.project_name = project['name']
        self.entrypoint = self.workdir + "/bin/" + self.project_name + '.ts'
        self.camel_case_name = camel_case(self.project_name)
        print(self.camel_case_name)
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
                        self.create_stage(ou, account, region)

    def create_stage(self, ou, account, region):
        # Create the directory tree
        print("Generating files for stage " + ou + "/" + account + "/" + region + "...")
        os.makedirs(self.workdir + "/src/stages/" + ou + "/" + account + "/" + region)

        # Create OU index
        if not os.path.isfile(self.workdir + "/src/stages/" + ou + "/index.ts"):
            print("Creating index file for ou... " + ou)
            create_file("templates/ou.template",
                        self.workdir + "/src/stages/" + ou + "/index.ts",
                        {
                            "ou": ou,
                            "class_name": camel_case(ou)
                        }
                        )
            print("Done.")
            print(" ")

        # Create Account index
        if not os.path.isfile(self.workdir + "/src/stages/" + ou + "/" + account + "/index.ts"):
            print("Creating index file for account " + account + "...")
            create_file("templates/account.template",
                        self.workdir + "/src/stages/" + ou + "/" + account + "/index.ts",
                        {
                            "parent_class": camel_case(ou),
                            "account": account,
                            "class_name": camel_case(ou) + camel_case(account)
                        }
                        )
            print("Done")
            print(" ")

        # Create Region index
        if not os.path.isfile(self.workdir + "/src/stages/" + ou + "/" + account + "/" + region + "/index.ts"):
            print("Creating index file for region " + region + " in account " + account + "...")
            create_file("templates/region.template",
                        self.workdir + "/src/stages/" + ou + "/" + account + "/" + region + "/index.ts",
                        {
                            "parent_class": camel_case(ou) + camel_case(account),
                            "region": region,
                            "class_name": camel_case(ou) + camel_case(account) + camel_case(region)
                        })
            print("Done")
            print(" ")

    def generate_region_configs(self):
        imports = []
        configs = []
        for region in self.regions:
            if not os.path.isfile(self.workdir + "/src/configuration/regions/" + region + ".ts"):
                print("Creating configuration file for region " + region + "...")
                create_file("templates/region-config.template",
                            self.workdir + "/src/configuration/regions/" + region + ".ts",
                            {
                                "region_name": camel_case(region)
                            })
                imports.append("import { config as " + camel_case(region) + "Config } from './" + region + "';")
                configs.append("['" + region + "']: " + camel_case(region) + "Config,")
                print("Done")
                print(" ")

        self.create_region_config_index(imports, configs)

    def create_region_config_index(self, imports, configs):
        print("Creating index file for region configurations...")
        create_file("templates/region-index.template",
                    self.workdir + "/src/configuration/regions/index.ts",
                    {
                        "imports": '\n'.join(imports),
                        "configs": '\n\t'.join(configs)
                    })
        print("Done")
        print(" ")

    def run_install(self):
        print("run install")
        install = subprocess.Popen(["npm", "install"], cwd=self.workdir)
        install.wait()


def main(name, path, config):
    cdk_project = StagedCdkProject(name, path, config)
    cdk_project.build()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',
                        help='Full path to directory to create project in.',
                        required=True)
    parser.add_argument('-n', '--name', help='Name of project to create.', default='AwesomeProject')
    parser.add_argument('-c', '--config', help='(Optional)Full path to config file that defines stages to create.', default=None)
    args = parser.parse_args()

    main(args.name, args.path, args.config)
