"""
Initializes a cdk application with directory structured for using stages.
"""
import argparse
import subprocess

import sys
import os

from .cdk_project import CdkProject
from .region_configuration import RegionConfiguration


def run_install(workdir):
    print("run install")
    install = subprocess.Popen(["npm", "install"], cwd=workdir)
    install.wait()


def main(name, path, conf, demo=False):
    if not path:
        workdir = os.getcwd() + "/" + name
    else:
        workdir = path + "/" + name

    project = CdkProject(name=name, workdir=workdir, demo=demo, configuration=conf)
    project.build()

    RegionConfiguration(workdir=workdir, regions=project.regions)

    run_install(workdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='cdk-stages', usage='python3 -m %(prog)s [options]')
    parser.add_argument('--sampleapp', help='Creates sample application.', action="store_true")

    parser.add_argument('-p', '--path',
                        help='Full path to directory to create project in.',
                        default=None)
    parser.add_argument('-n', '--name', help='Name of project to create.', default='AwesomeProject')
    parser.add_argument('-c', '--conf', help='Path to config that defines stages to create.',
                        default=None)
    args = parser.parse_args()

    demo = False

    main(args.name, args.path, args.conf, args.sampleapp)
