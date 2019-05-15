## Deployment

### Azure

Doccano can be deployed to Azure ([Web App for Containers](https://azure.microsoft.com/en-us/services/app-service/containers/) +
[PostgreSQL database](https://azure.microsoft.com/en-us/services/postgresql/)) by clicking on the button below:

[![Deploy to Azure](https://azuredeploy.net/deploybutton.svg)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fgong-io%2Fdoccano%2Fmaster%2Fazuredeploy.json)


## Installation

First of all, you have to clone the repository:

```bash
git clone https://github.com/gong-io/doccano.git
cd doccano
```

To install doccano, there are two options:

**Option1: Pull the Docker image**

```bash
docker pull gong-io/doccano
```

**Option2: Setup Python environment**

```bash
pip install -r requirements.txt
cd app
```

First we need to make migration. Run the following command:

```bash
python manage.py migrate
```

Next we need to create a user who can login to the admin site. Run the following command:


```bash
python manage.py createsuperuser
```

Enter your desired username and press enter.

```bash
Username: admin
```

You will then be prompted for your desired email address:

```bash
Email address: admin@example.com
```

The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.

```bash
Password: **********
Password (again): *********
Superuser created successfully.
```


## Tests
Doccano includes a suite of tests. 

To run tests:
[[TODO: Write this section]]
