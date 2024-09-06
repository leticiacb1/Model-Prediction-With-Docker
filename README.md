### 🐋️ Predict Lambda Function with Docker

**Docker** containers as an alternative deployment method helps to bypass lambda functions limitations, enabling more complex and scalable applications.

The `Amazon Elastic Container Registry (ECR)` is a fully managed service that allows you to store, manage, and deploy container images.

This project creates a docker image with a mock of a Machine Learning model prediction function. This function can be accessed using an API and returns a mock value when accessed.

#### 📌 Run the project

* **Dependencies** 

Install **AWS CLI**, [click here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

```bash
# Configure credentials
$ aws configure --profile mlops
AWS Access Key ID [None]: ????????????
AWS Secret Access Key [None]: ????????????????????????????????
Default region name [None]: us-east-2
Default output format [None]:

# Set profile in each terminal you will use
$ export AWS_PROFILE=mlops

# List the names of lambda functions associated with your account:
$ aws lambda list-functions --query "Functions[*].FunctionName" --output text
```
<br>

Create a `venv` and install dependencies:

```bash
    # Create environment
    python3 -m venv venv  

    # Activate environment
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
``` 

Create a `.env` file inside `config/` folder with user and password of RabbitMQ:

```bash
    # .env content'
    AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXX"
    AWS_SECRET_ACCESS_KEY="aaaaaaaaaaaaaaaaaaaaaaaaaaa"
    AWS_REGION="xx-xxxx-2"
    AWS_LAMBDA_ROLE_ARN="arn:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
``` 

* **Run the project** 

First create the Container Register in AWS, it will store our docker image. For this run the code : 

```bash
$ python3 create_repository.py
# Save the repository uri
```

> :warning: **Attention**
> 
> Now create your image with your source_code, in my case the function in `predict.py`, and upload in the _Container Register_. 
> 
> To do this, follow the _step-by-step_ instructions in the topic **How to create and upload a Docker image**.
> 

Now, let's create a lambda function from the image already stores in the ECR.

```bash
$ python3 create_lambda_function.py
```

> **_NOTE:_**
> Is possible that the lambda function still in **pending state** when your try to invoke.
> ```bash
> # Possible error when run python3 create_lambda_function.py
> An error occurred (ResourceConflictException) when calling the Invoke operation: 
> The operation cannot be performed at this time. The function is currently in the following state: Pending
> ```
> If this happen you can verify the state of the function and then try to call only the invoke part again.
> ```bash
> # Set the aws output method 
> $ aws configure set output json
> # Run to see the function state: 
> $ aws lambda get-function --function-name <function-name>
> ```
> When `state = Active`, run only this part of the code to see if the function is invoked successfully:
> ```python
> # file : create_lambda_function.py
> _lambda = LambdaFunction()
> _lambda.create_client()
> _lambda.check_function(function_name=function_name, input = function_input)
> _lambda.see_all_lambda_functions()
> ``` 

<br>

Create a API gateway:

```bash
$ python3 create_gateway.py
```

For test the lambda function run:


```bash

# Update the api_endpoint variable with the value of the api url
$ python3 predict_test.py
```

<br>

#### 🤔 How to create and upload a Docker image

Examples of Docker images [here](https://gallery.ecr.aws/lambda/python).
<br>

* Create a file named `Dockerfile`.

```dockerfile
FROM public.ecr.aws/lambda/python:3.10
RUN echo ' > Init dockerfile. '
RUN echo '   Using a aws/lambda/python3.10 image as base.'

# Copy requirements.txt
RUN echo ' > Copy requirements.txt ...'
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
RUN echo ' > Copy lambda function code ...'
COPY predict.py ${LAMBDA_TASK_ROOT}

# Install system dependencies
RUN echo ' > Install system dependencies ...'
RUN yum install -y libstdc++ cmake gcc-c++ && \
    yum clean all && \
    rm -rf /var/cache/yum

RUN echo ' > Install requirements.txt ...'
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
RUN echo ' > Defines the default executable of a Docker image as the lambda function ...'
CMD [ "predict.run" ]
```
<br>

* Build the image with a name and give it a _test_ tag:

```bash
    # In root of this project:
    # Dockerfile inside de onfig folder
    # lambda-ex-image is the name of the image
    docker build . --platform linux/amd64 -t aps3-leticiacb1:test -f config/Dockerfile 
```
<br>

* For see docker images:
```bash
    docker images

    # If you want to delete some image before 
    # create one with the same name run: 
    # $ docker rmi <image-id> --force
```

Example of expected output : 

|REPOSITORY  |    TAG     |   IMAGE ID    |   CREATED   |      SIZE    |
|------------|------------|---------------|-------------|--------------|
|aps3-leticiacb1 |      test |          00fcb2b3f7d5 |  About a minute ago  | 1.27GB |

<br>

* Test image locally

Open a terminal and run:

```bash
docker run -p 9500:8080 aps3-leticiacb1:test
```

In other terminal make a request, is expected to return the handler of lambda function:

```bash
curl -X POST "http://localhost:9500/2015-03-31/functions/function/invocations" \
-H "Content-Type: application/json" \
-d '{"body": "{\"person\":{\"argumento\":\"algo-aqui\"}}"}'
```

Now, let's upload this local image in the ECR AWS container.

First you need to have the _CLI AWS_ configured. (See **Run the project-First Steps**)

```bash
# Authenticate and login to ECR using the Docker CLI
# Change AWS_ACCOUNT_ID to your AWS account_id
# Change AWS_REGION to your AWS region credentials

# $ aws ecr get-login-password --region AWS_REGION | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com

$ aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 820926566402.dkr.ecr.us-east-2.amazonaws.com

# Expected output : Login Succeeded
```

```bash
# Tag the local Docker image into your Amazon ECR repository as the latest version.
# Change REPOSITORY_URI for your repository_uri
# The format of REPOSITORY_URI is like this : AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/REPOSITORY_NAME

# $ docker tag lambda-ex-image:test REPOSITORY_URI:latest

$ docker tag aps3-leticiacb1:test 820926566402.dkr.ecr.us-east-2.amazonaws.com/aps3-mlops-leticiacb1:latest

```

After run `docker images` again is expected to get:


|REPOSITORY  |    TAG     |   IMAGE ID    |   CREATED   |      SIZE    |
|------------|------------|---------------|-------------|--------------|
|aps3-leticiacb1 |      test |          00fcb2b3f7d5 |  About a minute ago  | 1.27GB |
| 820926566402.dkr.ecr.us-east-2.amazonaws.com/aps3-mlops-leticiacb1 |    latest |00fcb2b3f7d5 |  About a minute ago |  1.27GB |

Finally, push the image to ECR:

```bash
# $ docker push REPOSITORY_URI:latest
$ docker push 820926566402.dkr.ecr.us-east-2.amazonaws.com/aps3-mlops-leticiacb1:latest
```

Wait until the push finishes.

<br>

> :warning: _Error trying to do login on ECR_
> >
> Is possible that you get a error like this when you try to login:
> ```bash
> An error occurred (UnrecognizedClientException) when calling the GetAuthorizationToken operation: The security token included in the request is invalid.
>Error: Cannot perform an interactive login from a non TTY device
> ```
> First make sure that you have the **aws configure** and the **AWS profile exported** and with the rights to do this connection.
> ```bash
> # Check the profile used
> $ aws sts get-caller-identity
>```
> If you dont have the **gpg key** configure in your machine, configure
>
> ```bash
> # Check if you have a gpg key configured
> $ gpg --list-keys
> # If you dont have a gpg key configured create one:
> $ gpg --full-generate-key
>```
>
> Get your _gpg key id_ and run the command : 
> ```bash
> pass init <gpg-key-id>
> ```
> After that retry the Docker login command :
> ```bash
> aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 820926566402.dkr.ecr.us-east-2.amazonaws.com
> ```
> See more about this problem [here.](https://unix.stackexchange.com/questions/545772/error-cannot-perform-an-interactive-login-from-a-non-tty-device)
<br>



<br>
@2024, Insper. 9° Semester,  Computer Engineering.
<br>

_Machine Learning Ops & Interviews Discipline_