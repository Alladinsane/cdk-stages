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
        print("Building stages based on the config:  ")
        print(json.dumps(self.config, indent=2))
        regions = []
        for item in self.project_stages:
            for ou in item:
                for account in item[ou]:
                    for region in item[ou][account]:
                        regions+=region
                        self.create_stage(ou, account, region)

    def create_stage(self, ou, account, region):
        # Create the directory tree
        print("Generating files for stage "+ou+"/"+account+"/"+region+"...")
        os.makedirs(self.workdir + "/src/stages/" + ou + "/" + account + "/" + region)

        # Create OU index
        if not os.path.isfile(self.workdir+"/src/stages/"+ou+"/index.ts"):
            print("Creating index file for ou... " + ou)
            self.create_index("templates/ou.template",
                              self.workdir+"/src/stages/"+ou,
                              {
                                  "ou": ou,
                                  "class_name": camel_case(ou)
                              }
            )
            print("Done.")

        # Create Account index
        if not os.path.isfile(self.workdir+"/src/stages/"+ou+"/"+account+"/index.ts"):
            print("Creating index file for account " + account + "...")
            self.create_index("templates/account.template",
                              self.workdir + "/src/stages/" + ou + "/" + account,
                              {
                                  "parent_class": camel_case(ou),
                                  "account": account,
                                  "class_name": camel_case(ou) + camel_case(account)
                              }
            )
            print("Done")

        #Create Region index
        if not os.path.isfile(self.workdir+"/src/stages/"+ou+"/"+account+"/"+region+"/index.ts"):
            print("Creating index file for region " + region + " in account " + account + "...")
            self.create_index("templates/region.template",
                              self.workdir + "/src/stages/" + ou + "/" + account + "/" + region,
                              {
                                  "parent_class": camel_case(ou) + camel_case(account),
                                  "region": region,
                                  "class_name": camel_case(ou) + camel_case(account) + camel_case(region)
                              })
            print("Done")

    def create_index(self, template_path, target_path, args):
        with open(template_path) as t:
            template = string.Template(t.read())
        index = template.substitute(**args)
        with open(target_path+"/index.ts", "w") as output:
            output.write(index)

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