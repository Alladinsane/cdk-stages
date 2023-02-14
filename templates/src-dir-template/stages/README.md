# Overview

This directory contains the [Stages](https://docs.aws.amazon.com/cdk/v2/guide/cdk_pipeline.html#cdk_pipeline_stages) that make up the organization. A stage is a natural grouping of one account plus one region. This is because CloudFormation is a regional service so Stages represent the collection of all of the stacks that would be deployed to an individual account's region. When you go into that account's [CloudFormation console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks) in a particular region you will see all the stacks that were deployed that belong to that stage.

## Stack Inheritance

In order to reduce duplication of code and the potential for inconsistent configurations, we implement a system of [inheritance](https://en.wikipedia.org/wiki/Inheritance_%28object-oriented_programming%29) that allows stacks to be defined at various points and be inherited by any children that inherit from there. At its most basic, this inheritance tree looks like:

```
Organization > OU > Account > Region
```

Stacks can be added at any level of this tree and be applied to all layers underneath this. It is possible to have OU's inside of other OU's (nested OU's). In such a case the inheritance tree can likewise contain multiple OU's and any child OU will inherit all the stacks added to its parent.

**Example 1**
A stack is added to the constructor in the organization class at the root of the tree. This stack will be deplyed into every account and every region accross the entire organization.

This is something you might want to do for stacks that manage critical security and compliance resources you want to make sure get deployed everywhere.

**Example 2**
A stack is added to the constructor in a class that represents an Organizational Unit (OU). This stack will be deployed to every region in every account that is a child of this OU (or grandchild, great grandchild, etc).

This is something you might do for stacks that implement a common theme that all accounts in this OU share. An example of this is an OU that was configured for a specific client. All account's in this client's OU need to have VPC that a SaaS solution will be deployed into. Networks need to be deployed to both the primary and DR regions to be ready in the event that a failover is needed.

**Example 3**
A stack is added to the constructor in a class that represents an AWS account. This stack is deployed to every region in that AWS account.

This is something you might do for stacks that deploy shared resources that only need to be deployed to a single account across the entire organization but are regional and therefore need to be deployed to multiple regions. An example of this would be a stack that creates ECR repositories to store the Docker images built for your organization.

A single registry in a shared services account can provide a service's image for any account in the organization through use of [Resource Based Policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policies.html). However, ECR repositories are a regional service so you'd want to create one in every region and set up replication to ensure you are prepared in the event of a disaster scenario.

**Example 4**
A stack is added to the constructor of a class that represents an AWS region inside of a specific AWS account. Only one instance of this stack will be deployed and it'll be deployed to that specific account in that specific region.

This is something you might do for stacks that create clobal resources that only need to be deployed one time. Some example of this include a stack that sets up a Route 53 hosted zone that provides the domain all other resources in your organization are subdomains of, or a stack that deploys a role for a third party service (such as Gitlab) to assume to gather data or run commands within your organization.

Since both Route 53 and IAM are global services there is no need to deploy them to multiple regions for the sake of disaster recovery. Doing so would likely result in an error due to multiple resources with the same name being created.

# Directory Structure

The structure of this directory consists of a single code file in the root (`organization.ts`) and a directory heirarchy where each level represents an AWS OU, account, or region (inside of a specific account). Each directory is named after the component it represents (OU name, account name, or region name). All names are lower case and use hyphens (-) for word separation.

Inside each subdirectory is an `index.ts` file that contains a class representing that that component of the organization. Each class defined by these files should inherite from the class defined in the directory directly above it.

A visual example of the directory structure:

```
├── organization.ts (organization class)
├── clients (ou)
│   ├── index.ts (ou class)
│   └── client1 (nested ou)
│       ├── index.ts (nested ou class)
│       ├── dev (account)
│       │   ├── index.ts (account class)
│       │   ├── us-east-1 (region)
│       │   │   └── index.ts (region class)
│       │   └── us-east-2 (region)
│       │       └── index.ts (region class)
│       └── qa (account)
│           ├── index.ts (account class)
│           ├── us-east-1 (region)
│           │   └── index.ts (region class)
│           └── us-east-2 (region)
│               └── index.ts (region class)
└── shared (ou)
    ├── index.ts (ou class)
    └── services (account)
        ├── index.ts (account class)
        ├── us-east-1 (region)
        │   └── index.ts (region class)
        └── us-east-2 (region)
            └── index.ts (region class)
```

# Considerations and Challenges

## Cross account regional values

Some regional values should apply to every account in the organization. Examples of these are Transit Gateway ID's. A Transit Gateway can be shared between every account in a region, so every account in that region should know the same Transit Gateway ID. Typescript doesn't support multiple inheritance though, so these values can't simply be inherited depending on which region a stage is for.

To provide a solution to this, the `Organization` class, which serves as a parent class to all stages, provides a property called `regionConfig`. This `regionConfig` object is used to expose all values that apply across all accounts for a specific region. Regional config values can be added using the files in the `src/configuration/regions/` directory.

At runtime the organization retrieves the appropriate region configuration for the stage being run and exposes it to all the children inheriting from it.

## Abstract properties

Some configuration values are needed by parent classes but are not defined until one of the child classes does so. This can be problermatic as in TypeScript, abstract properties are not available to parent classes in the constructor. There are two ways to work around this:

* Use [Lazy evaluation](https://docs.aws.amazon.com/cdk/v2/guide/tokens.html#tokens_lazy) to consume the roperties that are not yet available. Instead of the value itself being passed, a token will be generated. When CDK produces its final output these Tokens will be evaluated and replaced with their actual values.
* Sometimes Lazy evaluation is not an option. This is the case when the value of a property needs to be known during the synthesis processes so that further processing on it can be applied. In these cases, abstract properties should be avoided. The property needed by the parent class should be made required by the parent class' props (values passed into the constructor) and child classes that inherit from it should pass the values up directly to make them available to the parent class.