# interlinked
What it's like to hold your data in your arms

## Baseline

When working with the L1000 dataset in a server environment I always felt something was missing.  Like I was locked out of a room.  The goal of interlinked is to enable fluid, seamless analysis of the LINCS L1000 dataset at scale leveraging the AWS Batch environment. It also provides a simple template for running R based analyses on AWS batch triggered by Lambda events. To find out all the answers to all the questions. Interlinked.

At this point, this is just a blood black darkness beginning to spin. Is that a metaphor? Interlinked.

## Creating lambda

The lambda requires (1) code, (2) IAM roles, and (3) API Gateway. Ideally also continuous integration with build and deployment triggered by pushes to your master repository via CodePipeline.  AWS CodeStar manages all of this for you seamlessly.  So begin by creating a project using CodeStar's Python/Web service/AWS Lambda template (or Node.js if you prefer).

