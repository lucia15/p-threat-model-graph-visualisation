# Running jupyter notebooks on Amazon Web Services (AWS)

### Step 1
Create an account on [AWS].

### Step 2
Log into your newly created AWS and navigate to the EC2 Dashboard. Click the launch Instance button.

![ec1](https://user-images.githubusercontent.com/8102313/102121329-e419c080-3e54-11eb-8d16-cb451249f87a.png)

### Step 3
Select Ubuntu distibution of your choice with "free tier eligible" For this demo I am choosing Ubuntu Server 20.04 LTS (HVM).
![ec2](https://user-images.githubusercontent.com/8102313/102122138-20015580-3e56-11eb-8ad2-d4db87d4a3fc.png)

### Step 4
Select t2.micro (Free tier eligible) and click the "Next: Configure Instance Details" Button.

### Step 5
Leave everything to default on the "Configure Instance Details" window and click the "Add Storage " Button.

### Step 6
![ec3](https://user-images.githubusercontent.com/8102313/102125704-22b27980-3e5b-11eb-98b6-0878d29b8877.png)

### Step 7
![ec4](https://user-images.githubusercontent.com/8102313/102126364-06fba300-3e5c-11eb-85d1-4c0af1244fd8.png)

### Step 8
![ec5](https://user-images.githubusercontent.com/8102313/102126953-dd8f4700-3e5c-11eb-8864-3492317afa5d.png)

### Step 9
Click on the "Review and Launch" button, then "Lauch" on the Next screen to create and download a security key.
![ec6](https://user-images.githubusercontent.com/8102313/102128187-8d18e900-3e5e-11eb-8a96-34e35c3afc84.png)

### Step 10
Click on Launch Instance, and then View Instance. Once opened, right click on the instance ID and select connect for instructions on how to connect to the instance remotely.
![ec7](https://user-images.githubusercontent.com/8102313/102129035-d0278c00-3e5f-11eb-9657-2b12b3c87fce.png)
eg. open your terminal, create a directory and copy the .pem file there. Inside the directory, run these cmds

```sh
$ chmod 400 my_key.pem
$ ssh -i "my_key.pem" ubuntu@ec2-3-16-160-15.us-east-2.compute.amazonaws.com
```
Type "yes" when prompted to continue.

### Step 11
Install and configure Anaconda

```sh
$ wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
$ bash Anaconda3-2020.11-Linux-x86_64.sh
```
Press enter a few times, Type ‘yes’ to agree and Press ENTER to confirm the location’

### Step 12
Create a password for jupyter notebook
```sh
$ ipython
$ from IPython.lib import passwd
$ passwd()
```
Enter password: [Create password and press enter] Verify password: [Press enter]
Copy the key generated somewhere and exit.

### Step 13
Create config profile and certificates for https
```sh
$ jupyter notebook --generate-config
$ mkdir certs
$ cd certs
$ openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout my_key.pem -out my_key.pem
```
Answer all the questions that follow as you see fit.

### Step 14
Configure jupyter
```sh
$ cd ~/.jupyter/
$ vi jupyter_notebook_config.py
```
Insert the following block  of code

c = get_config()
c.IPKernelApp.pylab = 'inline'  # if you want plotting support always in your notebook
c.NotebookApp.certfile = u'/home/ubuntu/certs/my_key.pem' #location of your certificate file
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.open_browser = False  #so that the ipython notebook does not opens up a browser by default
c.NotebookApp.password = u'sha1:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  #the encrypted password we saved in Step 12 above, Set the port to 8888, the port we set up in the AWS EC2 set-up
c.NotebookApp.port = 8888

Save and Exit.

### Step 15
Start Jupyter notebook
```sh
$ sudo chown $USER:$USER /home/ubuntu/certs/my_key.pem
$ jupyter notebook
```
Browser URL
https://ec2-3-16-160-15.us-east-2.compute.amazonaws.com:8888/

[AWS]: <https://aws.amazon.com/>
