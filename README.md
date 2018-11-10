# interlinked
What it's like to hold your data in your arms

## Baseline

When working with the L1000 dataset in a server environment I always felt something was missing.  Like I was locked out of a room.  The goal of interlinked is to enable fluid, seamless analysis of the LINCS L1000 dataset at scale leveraging the AWS Batch environment. It also provides a simple template for running R based analyses on AWS batch triggered by Lambda events. To find out all the answers to all the questions. Interlinked.

At this point, this is just a blood black darkness beginning to spin. Is that a metaphor? Interlinked.

## Running a job

Create a script from this template:

```
# these libraries are baked into the docker container
library(interlinker)
library(aws.s3)
library(httr)
library(jsonlite)

myfunc <- function(args) {
  mysum = args$a + args$b
  url <- paste0(interlinker_options("lambda_uri"), "upload")
  result <- POST(url, body = toJSON(list(key = "test/my_results_1",
                                         data = mysum,
                                         bucket = "interlinked"), auto_unbox = TRUE))
  # alternatively, you can just use aws.s3::put_object directly
  logS3(paste0("myfunc completed with result: ", result$result), "INFO", "interlinked")
}

```
This script should be uploaded to the `interlinked/scripts` bucket. In the future we will automate this step.

Then create a job description.  For our job above, we could use:

```
{
   "func": "myfunc",
   "arguments": {"a": 1, "b": 2},
   "name": "Test job",
   "script": "test.r"
}

```

We can then POST this job description to the script endpoint.  For example, in an R session:

```
library(interlinker)
library(jsonlite)
library(httr)

  job <- list(func = "myfunc",
   arguments =  list("a" = 1, "b" = 2),
   name = "Test job",
   script = "test.r")

  url <- paste0(interlinker_options("lambda_uri"), "submitjob")
  POST(url, body = toJSON(job), auto_unbox = TRUE))

```
That endpoint will save the job in S3 under a unique key. The lambda endpoint will then submit this job, setting the environment variable LAMBDA_JOB_ID to the UUID of this job description, and running `Rscript /tmp/start.r`, which is simply:

```
library(interlinker)

job <- Sys.getenv("LAMBDA_JOB_ID")
runJob(UUID, debug = TRUE)

```