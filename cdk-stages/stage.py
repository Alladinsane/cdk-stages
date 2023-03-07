import os

from . import utils
class Stage:
    def __init__(self, ou, account, region, workdir):
        self.ou = ou
        self.account = account
        self.region = region
        self.workdir = workdir

        self.create_stage()

    def create_stage(self):
        # Create the directory tree
        print("Generating files for stage " + self.ou + "/" + self.account + "/" + self.region + "...")
        os.makedirs(self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/" + self.region)

        # Create OU index
        if not os.path.isfile(self.workdir + "/src/stages/" + self.ou + "/index.ts"):
            print("Creating index file for ou... " + self.ou)
            utils.create_file("templates/ou.template",
                        self.workdir + "/src/stages/" + self.ou + "/index.ts",
                        {
                            "ou": self.ou,
                            "class_name": utils.camel_case(self.ou)
                        }
                        )
            print("Done.")
            print(" ")

        # Create Account index
        if not os.path.isfile(self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/index.ts"):
            print("Creating index file for account " + self.account + "...")
            utils.create_file("templates/account.template",
                        self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/index.ts",
                        {
                            "parent_class": utils.camel_case(self.ou),
                            "account": self.account,
                            "class_name": utils.camel_case(self.ou) + utils.camel_case(self.account)
                        }
                        )
            print("Done")
            print(" ")

        # Create Region index
        if not os.path.isfile(self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/" + self.region + "/index.ts"):
            print("Creating index file for region " + self.region + " in account " + self.account + "...")
            utils.create_file("templates/region.template",
                        self.workdir + "/src/stages/" + self.ou + "/" + self.account + "/" + self.region + "/index.ts",
                        {
                            "parent_class": utils.camel_case(self.ou) + utils.camel_case(self.account),
                            "region": self.region,
                            "class_name": utils.camel_case(self.ou) + utils.camel_case(self.account) + utils.camel_case(self.region)
                        })
            print("Done")
            print(" ")
