import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from .utils import create_file,camel_case
class Stage:
    def __init__(self, ou, account_name, account_connector, region, workdir, demo):
        self.ou = ou
        self.account = account_name
        self.account_connector = account_connector
        self.region = region
        self.workdir = workdir
        self.demo = demo

        if (self.account == 'account1') & self.demo & (self.region == 'us-east-1'):
            self.demo_env = '\n\t\tconst dev = new Environment(this, "dev", {\n\t\t\tname: "dev"\n\t\t})\n'
        else:
            self.demo_env = ""

        self.create_stage()

    def create_stage(self):
        # Create the directory tree
        print("Generating files for stage " + self.ou + "/" + self.account + "/" + self.region + "...")
        os.makedirs(self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/" + self.region)

        # Create OU index
        if not os.path.isfile(self.workdir + "/src/stages/" + self.ou + "/index.ts"):
            print("Creating index file for ou... " + self.ou)
            create_file("templates/ou.template",
                        self.workdir + "/src/stages/" + self.ou + "/index.ts",
                        {
                            "ou": self.ou,
                            "class_name": camel_case(self.ou)
                        }
                        )
            print("Done.")
            print(" ")

        # Create Account index
        if not os.path.isfile(self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/index.ts"):
            print("Creating index file for account " + self.account + "...")
            create_file("templates/account.template",
                        self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/index.ts",
                        {
                            "parent_class": camel_case(self.ou),
                            "account": self.account,
                            "class_name": camel_case(self.ou) + camel_case(self.account),
                            "account_connector": self.account_connector
                        }
                        )
            print("Done")
            print(" ")

        # Create Region index
        if not os.path.isfile(self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/" + self.region + "/index.ts"):
            print("Creating index file for region " + self.region + " in account " + self.account + "...")
            create_file("templates/region.template",
                        self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/" + self.region + "/index.ts",
                        {
                            "parent_class": camel_case(self.ou) + camel_case(self.account),
                            "region": self.region,
                            "class_name": camel_case(self.ou) + camel_case(self.account) + camel_case(self.region),
                            "demo_env": self.demo_env
                        })
            print("Done")
            print(" ")
