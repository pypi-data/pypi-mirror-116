Sklearn Tree for AWS SageMaker
============

This is an example project which builds small SKlearn Decision Tree model to create jobs with SageMaker. 

Prereqs.
-----

1. (3 minutes) awscli - To run mlctl with AWS, as end user, you will need to AWS CLI installed and authenticated. The most up to date instructions can be found on the [AWS CLI install page](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html). 

2. (10 minutes) Role assignments - To run a SageMaker job, you need to create an execution role. The role gives and limits which permissions the jobs created by mlctl can do. [This guide on the SageMaker docs](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html) include instructions for SageMaker and S3 access. You will see instructures to use this role in the `provider.yaml` below.

3. (5 minutes) Data Upload - SageMaker relies on S3 as the primary data source for inputs and outputs of each job. Create a S3 bucket in the same region you plan to run jobs in and upload in the `/data` folder of this tutorial. 

4. (3 minutes) Create a ECR Repo - Follow the (AWS instructions on creating an ECR repo)[https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html] . It is recommended to keep the region consistent with where you have your S3 bucket. 

5. (2 minutes) Docker - Have docker desktop or similar CLI on your local machine.

Usage
-----

1. Installation. 

Install the latest release of mlctl. This will also install mlbaklava, the packaging library used to build container jobs with your Python code. 

    ```
    pip install mlctl
    ```

2. Point mlctl to your infrastructure. 

Edit the `provider.yaml`. Replace `iam_arn_for_running_jobs` with your ARN role from the Step 2 prereqs. Replace the `container_repo_on_ECR` with the repo created in Step 4 of the prereqs. The `provider.yaml` file is an example of how the final should look. Our ECR repo is in us-east-1, but you could use another region.

    ```
    mlctl_version: 0.1
    infrastructure:
    - name: awssagemaker
      arn: arn:aws:iam::123456789:role/sagemaker-execution-role
      container_repo: 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker
    resources: 
      process: 'ml.t3.medium'
      train: 'ml.m5.large'
      deploy: 'ml.t2.medium'
    ```

3. Build the process job. 

Most models require data processing before it can be used. You can inspect the data processing code by navigating to `sklearn_tree/process.py`. The mapping of all the other job starting points can be found in `setup.py` entry_points. Mlctl is taking your code as an entrypoint and running bootstrap and post-job code that is required by the underlying MLOps infrastructure.

The code needs to be compiled to a container, which mlctl does automatically for you with a runtime utility called mlsriracha. To start the process, run the follow commands to build each jobs

    ```
    mlctl process build -c process.yaml
    
    ```

4. Upload process job container to ECR

ECR has a custom login script. To start that command, run `aws ecr get-login`. If you need to specify an AWS region, [read through the command options](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html#cli-authenticate-registry) in full.

    ```
    docker tag process-image 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:process-image
    docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:process-image
    ```

5. Define and run the process job

The process job takes a file, and then does simple filtering, and saves it back in another S3 directory. Edit the `process.yaml` with the S3 bucket you uploaded the Step 3 prereq above. The output can be a different folder in the same S3 bucket. Mlctl defines jobs by project, job name, data files, and inputs. For process jobs, typically the user inputs are minimal and the changed parameter is the data source.

```
mlctl_version: 0.1
metadata:
  version: 1.0
  project: weight_data_aws
  job_type: process
data:
  input: s3://mlctltest/example1_data/
  output: s3://mlctltest/example1_data_out/
```
After the `process.yaml` has been changed, the process job can be run

    ```
    mlctl process start -c process.yaml
    ```

6. Build, upload, and run the Train job

The training job requires a similar compilation step. Replace the 

    ```
    mlctl train build -c train.yaml
    docker tag train-image 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:train-image
    docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:train-image
    ```

The training job yaml in `train.yaml` requires the data inputs and outputs be updated with your S3 bucket. 

7. Build, upload, and create a model endpoint
    ```
    docker tag deploy-image 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:deploy-image
    docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:deploy-image
    mlctl deploy build -c deploy.yaml
    ```

    This will host the prediction function on your local machine
    identically to how it would be hosted in sagemaker.

8. Test the endpoint

Find the name of the endpoint by checking the logs. The patterns is XXXXXXXXX, and replace the `endpoint_name_value` below with the SageMaker provided endpoint name.

```
aws sagemaker invoke-endpoint
--endpoint-name <endpoint_name_value>
--body {"instances":[{"age": 35, "height": 182}]}
```