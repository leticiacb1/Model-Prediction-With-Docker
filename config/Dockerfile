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