[![CircleCI](https://circleci.com/gh/asn10038/AutoIntern-Django.svg?style=svg)](https://circleci.com/gh/asn10038/AutoIntern-Django)
---
# AutoIntern

A banking workflow app with more to come. Currently under construction.
https://autointern-prod.appspot.com/
---
# Set Up

### Git Clone
Here we are cloning the repo to your file system
1. Open Terminal
2. Navigate to where you want this repo
3. "git clone https://github.com/asn10038/AutoIntern-Django.git"

### Create a Git Branch And Open a Pull Request
Note: ALL WORK should be done on an individualized dev branch and should be submitted as a pull request to the "dev" branch.
1. Switch to your dev branch using "git checkout -b <name>_dev", i.e. nick_dev.
2. Edit, add, and commit code as normal (use informational commit messages).
3. When you are ready to push changes use "git push -u origin <name>_dev". Note: I believe you will only have to do this the first time and then you can use "git push" as usual.
5. Navigate to https://github.com/asn10038/AutoIntern-Django and go to "Pull Requests" and create one from your dev branch to the "dev" branch. Make sure to assign people to the pull request and don't accept your own PR.
6. After fixing any PR merge conflicts in "dev" support a PR from "dev" to "master".

### Making A Virtual Enviornment
Here we are making a virtual enviornment to make sure the enviornment we are coding in is standard across all programmers. All of your local testing should be done in the virtual enviornment. More info: https://www.python.org/dev/peps/pep-0405/
1. In /AutoIntern-Django type "python3 -m venv autointernvenv". This creates an enviornment called autointernvenv at /AutoIntern-Django. You need to do this once. Note: You will see a directory called autointernvenv, this stores the enviornment. Don't mess with it. It will also not be committed because it is in our .gitignore file.
2. Type "source autointernvenv/bin/activate" to activate the environment. Your commandline will change to note that the enviornment is different than default. All coding and testing should be done with this enviornment. (so you'll have to use this command every time you make changes or test).
3. Type "pip install -r requirements.txt". This downloads the packages in our enviornment to the enviornment on your machine. You will only have to run this command when the requirements.txt changes (and when setting up the enviornment).
4. To deactivate the enviornment type "deactivate".
5. If there is a package you want/need to use, add it to the "requirements.txt" file and add that in your commit as well.

### Start The Database Proxy
This connects your local machine to the dev database for local testing. You can elect to not test locally and push to the "dev" branch whenever you want circleci to run tests. And can go to the dev website (after circleci has automatically deployed your push) to interact with/view it.  However, to run the code locally you will have to first start the database proxy.
1. Follow the instructions here <a href='https://cloud.google.com/sdk/downloads#interactive'>Google Cloud SDK</a> for downloading the interactive installer. You will have to do this once.
2. Type "gcloud init" in your terminal, you should have to follow some steps such as login in to your email, and then should be allowed to select a default project and should have the options of our dev, uat, and prod projects. Select the dev project.
2. To start the Proxy, go to /AutoIntern-Django and type "./cloud_sql_proxy_unix -instances="autointern-dev:us-east1:autointern-dev"=tcp:5432" if on a unix machine (mac) and "./cloud_sql_proxy_linux -instances="autointern-dev:us-east1:autointern-dev"=tcp:5432" if on a linux machine. Leave this running to test the code locally.

### Start the Application
Here we will run the application and allow you to connect to it locally.
1. Make sure you have the database proxy running in another terminal window.
2. Make sure your virtual environment is active and you are in /AutoIntern-Django.
3. Type "python manage.py runserver".
4. Go to "http://localhost:8000/" to see the website.

### Run All Tests
Using Django there is a handy trick to running all of the tests written.
1. "python manage.py test"


## Licensing

TODO
