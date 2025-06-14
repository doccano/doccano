# Setup cloud storage

This document explains how to setup cloud storages to store the imported datasets to the cloud storage. The following cloud storages are supported in doccano:

- [Amazon S3](#amazon-s3)
- [Google Cloud Storage](#google-cloud-storage)

## Amazon S3

The steps of connecting your Amazon S3 bucket to doccano to store the imported datasets.

- [Create credentials](#create-credentials)
- [Create a bucket](#create-a-bucket)
- [Create a .env file](#create-a-env-file)

### Create credentials

You must provide your AWS access keys to make programmatic calls to AWS.

When you create your access keys, you create the access key ID (for example, AKIAIOSFODNN7EXAMPLE) and secret access key (for example, wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY) as a set. The secret access key is available for download only when you create it. If you don't download your secret access key or if you lose it, you must create a new one.

1. Sign in to the AWS Management Console as an IAM user.
2. In the navigation bar on the upper right, choose your user name and then choose **My Security Credentials**.
3. To create an access key, choose **Create access key**. If you already have two access keys, this button is disabled and you must delete an access key before you can create a new one. When prompted, choose either **Show secret access key** or **Download .csv file**. This is your only opportunity to save your secret access key. After you've saved your secret access key in a secure location, chose **Close**.

### Create a bucket

To store your dataset to Amazon S3, you must first create an Amazon S3 bucket in one of the AWS Regions. When you create a bucket, you must choose a bucket name and Region. You can optionally choose other storage management options for the bucket. After you create a bucket, you cannot change the bucket name or Region.

1. Sign in to the AWS Management Console and open the Amazon S3 console.
2. Choose **Create bucket**.
3. In Bucket name, enter a name for your bucket(e.g. doccano).
4. In Region, choose the AWS Region where you want the bucket to reside. Choose a Region close to you to minimize latency and costs and address regulatory requirements.
5. Under Object Ownership, to disable or enable ACLs and control ownership of objects uploaded in your bucket, choose **ACLs disabled**.
6. In Bucket settings for Block Public Access, choose the **Block Public Access** settings that you want to apply to the bucket.
7. Choose **Create bucket**.

### Create a .env file

Once you create a credential and a bucket, you must create a `.env` file:

```bash
DJANGO_SETTINGS_MODULE=config.settings.aws
AWS_ACCESS_KEY_ID={SET_YOUR_KEY}
AWS_SECRET_ACCESS_KEY={SET_YOUR_SECRET_KEY}
REGION_NAME=us-west-1
BUCKET_NAME=doccano
```

## Google Cloud Storage

The steps of connecting your Google Cloud Storage bucket to doccano to store the imported datasets.

- [Create credentials](#create-credentials-1)
- [Create a .env file](#create-a-env-file-1)

### Create credentials

Create a service account:

1. In the Cloud Console, go to the [Create service account](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts/create) page.
2. Select your project.
3. In the **Service account name** field, enter a name. The Cloud Console fills in the **Service account ID** field based on this name. In the **Service account description** field, enter a description. For example, Service account for quickstart.
4. Click **Create and continue**.
5. To provide access to your project, grant the following role(s) to your service account: **Cloud Storage > Storage Admin**.
6. Click **Continue**.
7. Click **Done** to finish creating the service account. Do not close your browser window. You will use it in the next step.

Create a service account key:

1. In the Cloud Console, click the email address for the service account that you created.
2. Click **Keys**.
3. Click **Add key**, then click **Create new key**.
4. Click **Create**. A JSON key file is downloaded to your computer.
5. Click **Close**.

### Create a .env file

Once you create a credential and a bucket, you must create a `.env` file. Notice that the file contents differ slightly between the Pip and Docker versions:

```bash
DJANGO_SETTINGS_MODULE=config.settings.gcp
GS_PROJECT_ID={SET_YOUR_PROJECT_ID}
BUCKET_NAME=doccano
# In the case of Pip
GOOGLE_APPLICATION_CREDENTIALS={SET_CREDENTIAL_PATH}
# In the case of Docker
GOOGLE_APPLICATION_CREDENTIALS=/doccano/{SET_CREDENTIAL_PATH}
```

## Run doccano with the .env file

### Pip

When you execute the `webserver` and `task` command, specify `--env_file` option:

```bash
doccano webserver --env_file=.env
doccano task --env_file=.env
```

### Docker

When you execute the `docker container create` command, specify `--eng-file` option:

```bash
# Create a container
docker container create --name doccano \
  -e "ADMIN_USERNAME=admin" \
  -e "ADMIN_EMAIL=admin@example.com" \
  -e "ADMIN_PASSWORD=password" \
  -v doccano-db:/data \
  --env-file .env \
  -p 8000:8000 doccano/doccano

# Notice that you must copy the credential in the case of Google Cloud Storage
docker cp {CREDENTIAL_PATH} doccano:/doccano/

# Start the container
docker container start doccano
```

## References

- [Understanding and getting your AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)
- [Amazon S3/Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)
- [Google Cloud/Getting started with authentication](https://cloud.google.com/docs/authentication/getting-started)
