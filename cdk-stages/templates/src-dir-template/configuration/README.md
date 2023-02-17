# Overview

This directory is used for defining static configuration values that couldn't be defined along with individual constructs or would either be too unwieldy to do so.

# Directory Structure

File names should be all lower case with words separated by hyphens. If a file defines a class, the file name should match the name of the calss it defines. Further organization can be done into subdirectories if it makes sense to do so.

# Notable Configurations

## Cost centers

The cost centers configurations attempts to break down AWS resource types into broad cost centers for the sake of tagging. These cost center tags can be used in billing reports to get a general sense of where money is being spent. A general example of this is the cost center for "network" containing all AWS resource types that are generally most associated with providing networking functionality.

The lists provided in this configuration are non-exhaustive and will likely need to be tweaked, expanded, and refined as time goes by and new services are added and the needs of the organization shift.

## Regions

Some regional values should apply to every account in the organization. Examples of these are Transit Gateway ID's. A Transit Gateway can be shared between every account in a region, so every account in that region should know the same Transit Gateway ID. Typescript doesn't support multiple inheritance though, so these values can't simply be inherited depending on which region a stage is for.

To provide a solution regional values can be configured here. When a [Stage](https://docs.aws.amazon.com/cdk/v2/guide/cdk_pipeline.html#cdk_pipeline_stages) is created it will automatically pull the region-wide configuration for its region defined here. These values will then be exposed for stacks and resources that are being added to the stage via the `regionConfig` property.