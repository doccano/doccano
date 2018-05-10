# doccano

doccano is a document annotation tool. The purpose is making annotation process efficient. First, manually labeling small data in minutes using the labeling interface. Second, train built-in classification model using the labeled data and classify unlabeled data with their probability. Then, sort data in ascending order by the probability. You can efficiently annotate the data.

![doccano](docs/placeholder.png)

<!--
## Demo
-->

## Features

* Active Learning based annotation

## Requirements

* Python3.6+
* numpy 1.14.3+
* scikit-learn 0.19.1+
* scipy 1.1.0+

Put data into [doccano/data](https://github.com/chakki-works/doccano/tree/master/data) directory.

## Installation

To install namaco, simply run:

```bash
$ git clone https://github.com/chakki-works/doccano.git
$ cd doccano
$ pip install -r requirements.txt
```

## Usage

First, run web application:

```bash
$ cd doccano/server
$ python run_server.py
```

Then, open <http://localhost:8080> in your browser.
