# Overview

Files in this directory provide additional functionality used by constructs in the CDK without actually directly defining [Constructs](https://docs.aws.amazon.com/cdk/v2/guide/constructs.html) themselves. This could be a function that performs complex processing logic and a value that is used by multiple other classes or an [Aspect](https://docs.aws.amazon.com/cdk/v2/guide/aspects.html) that performs some for of post-processing but doesn't make sense to incorporate into a construct itself.

# Directory Structure

File names should be all lower case with words separated by hyphens. If a file defines a class, the file name should match the name of the calss it defines. Further organization can be done into subdirectories if it makes sense to do so.