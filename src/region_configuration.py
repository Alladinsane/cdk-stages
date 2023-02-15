import os

from utils import create_file, camel_case


class RegionConfiguration:
    def __init__(self, workdir, regions):
        self.workdir = workdir
        self.regions = regions

        self.imports = []
        self.configs = []

        self.create_region_configs()
        self.create_region_config_index()

    def create_region_configs(self):
        for region in self.regions:
            if not os.path.isfile(self.workdir + "/src/configuration/regions/" + region + ".ts"):
                print("Creating configuration file for region " + region + "...")
                create_file("templates/region-config.template",
                            self.workdir + "/src/configuration/regions/" + region + ".ts",
                            {
                                "region_name": camel_case(region)
                            })
                self.imports.append("import { config as " + camel_case(region) + "Config } from './" + region + "';")
                self.configs.append("['" + region + "']: " + camel_case(region) + "Config,")
                print("Done")
                print(" ")

    def create_region_config_index(self):
        print("Creating index file for region configurations...")
        create_file("templates/region-index.template",
                    self.workdir + "/src/configuration/regions/index.ts",
                    {
                        "imports": '\n'.join(self.imports),
                        "configs": '\n\t'.join(self.configs)
                    })
        print("Done")
        print(" ")