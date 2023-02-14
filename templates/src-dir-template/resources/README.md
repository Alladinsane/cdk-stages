# Overview

This directory should be used for specifying [Resource](https://docs.aws.amazon.com/cdk/v2/guide/resources.html) constructs that can be added to various [Stacks](https://docs.aws.amazon.com/cdk/v2/guide/stacks.html). 

Stack provide a grouping of resources that all come together to perform a logical grouping to be deployed together. Generally speaking, most low level interaction between AWS components should be separated into [Resource constructs](https://docs.aws.amazon.com/cdk/v2/guide/resources.html) instead of being added to the stack directly.

The distinction of which groupings should be made into a resource and which should be made into a stack is somewhat nuanced and open to interpretation. As a general rule though, Resources should be used to group together a lot of individual AWS components to form a single logical unit of work, while stacks should group resources that share a common theme or idea.

A good example of the distinction would be a VPC resource, which contains a VPC itself, subnets, route tables, network ACL's, gateways, and anything else that pretty much comes with every VPC being deployed. This VPC _resource_ could then be added to a network _stack_ which groups all network related resources such as VPC, DNS, VPN's, into a single deployable group of resources.

# Directory Structure

This should primarily be a single flat directory with files added for every resource. Each file should contain one resource class and any helper elements (interfaces, enums, etc) that are used to interact with that class. The file name should match the name of the class it defines, with the name being converted to lower case and using hyphens to separate words.