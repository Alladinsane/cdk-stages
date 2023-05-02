# Cdk-Stages
python
## Summary
Rapidly deploys a typescript cdk project with a directory structured for implementing Stages. It includes a construct for 
creating Environments, basic structure for regional configurations, and defines some groupings of resource types into 
CostCenters.

This follows a pattern suitable for managing multi-account deployments for users that already utilize AWS Organizations. 
It utilizes stack inheritance to limit code duplication and centralize configuration of each stage.

## Requirements
- CDK
- npm
- python 3

## Installation
Cdk-Stages is an experimental project, which can be downloaded and run as a module using pip.

Clone the project, and install in *editable* mode.
```shell
pip install -e /path/to/cdk_stages
```

## Usage
For usage information:
```shell
python -m cdk-stages -h
```
```shell
usage: python -m cdk-stages [options]

options:
  -h, --help            show this help message and exit
  --sampleapp           Creates sample application.
  -p PATH, --path PATH  Full path to directory to create project in. Defaults to current working directory.
  -n NAME, --name NAME  Name of project to create.
  -c CONF, --conf CONF  Path to config that defines stages to create.
```
All arguments are optional. If no configuration is provided, no stages will be generated unless creating the sampleapp.

## Project Structure
Cdk-Stages generates projects by first executing `cdk init --app language=typescript` and then utilizing 
the templates and directories included to alter the structure. 

The entrypoint, bin/cdk.ts, is rewritten so that it is ready to begin defining stages. The lib directory is renamed to 
src, and laid out as shown in the example below.

```
├── src
│   ├── configuration
│   │   ├── cost-centers.ts
│   │   ├── README.md
│   │   └── regions
│   │       ├── index.ts
│   │       ├── region-base.ts
│   │       ├── us-east-1.ts
│   │       └── us-east-2.ts
│   ├── constructs
│   │   └── environment.ts
│   ├── resources
│   │   └── README.md
│   ├── stacks
│   │   └── README.md
│   ├── stages
│   │   ├── example
│   │   │   ├── index.ts
│   │   │   └── stage
│   │   │       ├── index.ts
│   │   │       ├── us-east-1
│   │   │       │   └── index.ts
│   │   │       └── us-east-2
│   │   │           └── index.ts
│   │   ├── organization.ts
│   │   └── README.md
│   └── utils
│       └── README.md
```

The exact names and contents of each stage directory and region configurations are generated based on the stages defined 
in the config, if one was provided. As shown, each directory contains a detailed README.

For detailed explanations of why we use this layout, and how it allows us to use stack inheritance to limit code 
duplication, see the READMEs in each directory. The best jumping off point is the 
[README on stages](./templates/src-dir-template/stages/README.md).

## Project Configuration
The project stages and empty region configurations are generated based on the stages defined in the configuration file. 
The configuration file should be a json list of objects defining all OUs, Accounts, and Regions in the project in the 
format:
```json
[
  {
    "name": "org_name",
    "accounts": [
      {
        "name": "account_name",
        "account_id": "1234567890",
        "regions": [
            "aws-region-code",
            ...
        ]
      },
      ...
    }
  }
]
```