import argparse
import os
import subprocess

from . import cdk_project
from . import region_configuration


def run_install(workdir):
    print("run install")
    install = subprocess.Popen(["npm", "install"], cwd=workdir)
    install.wait()


def main(name, path, config):
    if not path:
        workdir = os.getcwd() + "/" + name
    else:
        workdir = path + "/" + name

    project = cdk_project.CdkProject(name=name, workdir=workdir, configuration=config)
    project.build()

    region_configuration.RegionConfiguration(workdir=workdir, regions=project.regions)

    run_install(workdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',
                        help='Full path to directory to create project in.',
                        default=None)
    parser.add_argument('-n', '--name', help='Name of project to create.', default='AwesomeProject')
    parser.add_argument('-c', '--config', help='(Optional)Full path to config file that defines stages to create.',
                        default=None)
    args = parser.parse_args()

    main(args.name, args.path, args.config)
