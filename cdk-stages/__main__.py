import argparse
import os
import subprocess

from .cdk_project import CdkProject
from .region_configuration import RegionConfiguration


def run_install(workdir):
    print("run install")
    install = subprocess.Popen(["npm", "install"], cwd=workdir)
    install.wait()


def main(name, path, conf):
    if not path:
        workdir = os.getcwd() + "/" + name
    else:
        workdir = path + "/" + name

    project = CdkProject(name=name, workdir=workdir, configuration=conf)
    project.build()

    RegionConfiguration(workdir=workdir, regions=project.regions)

    run_install(workdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='cdk-stages', usage='python3 -m %(prog)s [options]')
    parser.add_argument('-p', '--path',
                        help='Full path to directory to create project in.',
                        default=None)
    parser.add_argument('-n', '--name', help='Name of project to create.', default='AwesomeProject')
    parser.add_argument('-c', '--conf', help='(Optional)Path to config that defines stages.',
                        default=None)
    args = parser.parse_args()

    main(args.name, args.path, args.conf)
