# Cdk-Stages
python
## Summary
Rapidly deploys a typescript cdk project that implements stages, an environment construct, and regional configurations. 
This follows a pattern suitable for managing multi-account deployments for users that already utilize AWS Organizations. 
It utilizes stack inheritance to limit code duplication and centralize configuration of each stage.

## Requirements
Requires CDK and npm.

## Usage
```shell
usage: cdk-stages [-h] -p PATH [-n NAME] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Full path to directory to create project in.
  -n NAME, --name NAME  Name of project to create.
  -c CONFIG, --config CONFIG
                        (Optional)Full path to config file that defines stages to create.
```

## Project Structure
Projects generated with cdk-stages are created by first executing `cdk init --app language=typescript` and then utilizing 
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
in your config. As shown, each directory contains a detailed README.

For detailed explanations of why we use this layout, and how it allows us to use stack inheritance to limit code 
duplication, see the READMEs in each directory. The best jumping off point is the 
[README on stages](./templates/src-dir-template/stages/README.md).
