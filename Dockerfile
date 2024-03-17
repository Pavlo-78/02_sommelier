# Use an official image1
FROM python:3.10

# Create a folder at the container root and copy files there from project
RUN mkdir /_appn
COPY ./_appn /_appn
# Create a folder at the container root and copy files there from project
RUN mkdir /_sqlapi
COPY ./_sqlapi /_sqlapi
# Copy files to container root from project root 
COPY ./requirements.txt /
COPY ./wine.db /

# Install the project dependencies
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Check the OS version of container, workdir and showing directory tree
RUN sh -c "cat /etc/os-release" 
RUN pwd
# Install tree command for showing tree catalogs in container
RUN apt-get update && apt-get install -y tree

WORKDIR /_appn
RUN tree 

# Run the app.py file when the container launches
WORKDIR /_appn
CMD ["uvicorn", "app1:app88", "--host", "0.0.0.0", "--port", "8000"]