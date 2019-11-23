# Welcome to doccano

## Text Annotation for Humans

doccano is an open source text annotation tool built for human beings. It provides annotation features for text classification, sequence labeling and sequence to sequence. So, you can create labeled data for sentiment analysis, named entity recognition, text summarization and so on. Just create project, upload your data and start annotating. You can build a dataset in hours.


## Demo

You can enjoy this [annotation demo](http://doccano.herokuapp.com).

### [Named entity recognition](https://doccano.herokuapp.com/demo/named-entity-recognition/)

First demo is one of the sequence labeling tasks, named-entity recognition. You just select text spans and annotate them. Since doccano supports shortcut keys, you can quickly annotate text spans.

![Named Entity Recognition](./named_entity_annotation.gif)

### [Sentiment analysis](https://doccano.herokuapp.com/demo/text-classification/)

Second demo is one of the text classification tasks, topic classification. Since there may be more than one category, you can annotate multi-labels.

![Text Classification](./text_classification.gif)

### [Machine translation](https://doccano.herokuapp.com/demo/translation/)

Final demo is one of the sequence to sequence tasks, machine translation. Since there may be more than one responses in sequence to sequence tasks, you can create multiple responses.

![Machine Translation](./translation.gif)

## Quick Deployment

### Azure

Doccano can be deployed to Azure ([Web App for Containers](https://azure.microsoft.com/en-us/services/app-service/containers/) +
[PostgreSQL database](https://azure.microsoft.com/en-us/services/postgresql/)) by clicking on the button below:

[![Deploy to Azure](https://azuredeploy.net/deploybutton.svg)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fchakki-works%2Fdoccano%2Fmaster%2Fazuredeploy.json)

### Heroku

Doccano can be deployed to [Heroku](https://www.heroku.com/) by clicking on the button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Of course, you can deploy doccano by using [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli).

```bash
heroku create
heroku stack:set container
git push heroku master
```

### AWS

Doccano can be deployed to AWS ([Cloudformation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)) by clicking on the button below:

[![AWS CloudFormation Launch Stack SVG Button](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3-external-1.amazonaws.com/cf-templates-10vry9l3mp71r-us-east-1/20190732wl-new.templatexloywxxyimi&stackName=doccano)

> Notice: (1) EC2 KeyPair cannot be created automatically, so make sure you have an existing EC2 KeyPair in one region. Or [create one yourself](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair). (2) If you want to access doccano via HTTPS in AWS, here is an [instruction](https://github.com/chakki-works/doccano/wiki/HTTPS-setting-for-doccano-in-AWS).
