## I can't install doccano.

Following list is ordered by from easy to hard. If you are not familiar with Python development, please consider easy setup.

1. [One click deployment to Cloud Service.](https://github.com/chakki-works/doccano#deployment)
    * Only you have to do is create an account. Especially [Heroku](https://www.heroku.com/home) does not require your credit card (if free plan).
    * [![Deploy to Azure](https://azuredeploy.net/deploybutton.svg)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fchakki-works%2Fdoccano%2Fmaster%2Fazuredeploy.json)
    * [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
    * [![AWS CloudFormation Launch Stack SVG Button](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3-external-1.amazonaws.com/cf-templates-10vry9l3mp71r-us-east-1/20190732wl-new.templatexloywxxyimi&stackName=doccano)
    * > Notice: (1) EC2 KeyPair cannot be created automatically, so make sure you have an existing EC2 KeyPair in one region. Or [create one yourself](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair). (2) If you want to access doccano via HTTPS in AWS, here is an [instruction](https://github.com/chakki-works/doccano/wiki/HTTPS-setting-for-doccano-in-AWS).
2. [Use Docker](https://docs.docker.com/install/)
    * Docker doesn't bother you by the OS, Python version, etc problems. Because an environment for application is packed as a container.
    * Get doccano's image: `docker pull chakkiworks/doccano`
    * Create & Run doccano container: `docker run -d --name doccano -p 8000:80 chakkiworks/doccano`
    * Create a user: `docker exec doccano tools/create-admin.sh "admin" "admin@example.com" "password"`
    * Stop doccano container: `docker stop doccano`
    * Re-Launch doccano container: `docker start doccano`
3. Install from source
    * **I want to remember you that this is the hardest setup way. You have to install Python/Node.js and type many commands.**
    * [Install Python](https://www.python.org/downloads/)
    * [Install Node.js](https://nodejs.org/en/download/)
    * Get the source code of doccano: `git clone https://github.com/chakki-works/doccano.git`
    * Move to doccano directory: `cd doccano`
    * Create environment for doccano: `virtualenv venv`
    * Activate environment: `source venv/bin/activate`
    * Install required packages: `pip install -r requirements.txt`
    * Move server directory: `cd app/server`
    * Build frontend library: `npm install`
    * Build frontend source code: `npm run build`
    * Back to server directory: `cd ../`
    * Initialize doccano: `python manage.py migrate`
    * Create user: `python manage.py createsuperuser`
    * Run doccano: `python manage.py runserver`
    * Stop doccano: Ctrl+C
    * Re-Launch doccano: `python manage.py runserver` (Confirm you are at `app/server` directory and environment is active).

## I can't upload my data.

Please check the following list.

- File encoding: `UTF-8` is appropriate.
- Filename: alphabetic file name is suitable.
- File format selection: File format radio button should be selected properly.
- When you are using JSON/JSONL: Confirm JSON data is valid.
  - You can use [JSONLint](https://jsonlint.com/) or some other tool (when JSONL, pick one data and check it).
- When you are using CSV: Confirm CSV data is valid.
  - You can use Excel or some tools that have import CSV feature. 
- Lack of line: Data file should not contain blank line.
- Lack of field: Data file should not contain blank field.

**You don't need your real & all data to validate file format. The picked data & masked data is suitable if your data is large or secret.**

## I want to add annotators.

* You can create other annotators by [Django Admin site](https://djangobook.com/django-admin-site/).
