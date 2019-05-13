# doccano

[![Build Status](https://travis-ci.org/chakki-works/doccano.svg?branch=master)](https://travis-ci.org/chakki-works/doccano)

Creating high-quality labels for a proprietary dataset is challenging, time consuming and expensive. Doccano is an open-source platform for the classification of text, images and audio that significantly reduces the time it takes to train machine learning models on real datasets by integrating Active Learning and Guided Search.

Doccano provides annotation features for text classification, sequence labeling, sequence to sequence, image classification, image labeling and audio classification, and can be easily extended to new types of annotation tasks. Using Doccano, you can create labeled data for sentiment analysis, named entity recognition, text summarization and so on. Just create a new project, upload your data and start annotating.

Doccano prompts labelers to annotate examples that would most likely improve model performance, leading to a significant reduction in the number of labeled examples required. Keyword search is available for text documents, leading to faster generation of annotated datasets that are expanded by machine learning algorithms even for highly imbalanced datasets.

Doccano allows for the integration of the work of multiple labelers, and provides administrative tools to for evaluating the performance of each labeler as well as inter-labeler agreement. It further combines the labelers annotations to create a joint gold standard.

## Video
((((EMBED A VIDEO SHOWING HOW DOCCANO WORKS))))

## Demo

You can play with an online demo version of Doccano [here](http://doccano.herokuapp.com).

## Use Cases

### [Sentiment analysis](https://doccano.herokuapp.com/demo/text-classification/)

Second demo is one of the text classification tasks, topic classification. Since there may be more than one category, you can annotate multi-labels.

![Text Classification](./docs/text_classification.gif)

### [Named entity recognition](https://doccano.herokuapp.com/demo/named-entity-recognition/)

In named-entity recognition projects you mark part of the text and annotate it as one of the available labels. A common use case is annotating people, places, company names etc. in text documents.

![Named Entity Recognition](./docs/named_entity_annotation.gif)

### [Sequence to Sequence & Machine translation](https://doccano.herokuapp.com/demo/translation/)

In Sequence-to-sequence (aka seq2seq) models you provide text that matches the original text. A common use case is machine translation - you are given a sentence in French, and need to translate it to English. Since there may be more than one responses in sequence to sequence tasks, you can create multi responses.

![Machine Translation](./docs/translation.gif)

## Features

* Collaborative annotation
* Language independent
* Active learning
* Guided search - filter results by matching text (e.g. a search for `"i will share" –screen` will return only documents with exact match of "i will share" and without the word "screen"). This allows fast labeling of documents with very high probability of belonging to a certain class.
* Admin reports about labels and labelers
  * View each labeler’s performance on ground truth
  * Retrain low-performing labelers
  * Identify unclear guidelines
  * Calculate inter-rater agreement (loosely associated with a limit to model performance)
  * Compute the labeling speed of each labeler
  * Estimate effort required to create a certain dataset size
* Filter records according to metadata
* Export of annotations to CSV
* Explain mode, highlighting words & phrases that might indicate a certain class, for faster annotation
* Increased productivity using keyboard shortcuts

## Technological Stack
Doccano is built in Django, a popular Python framework for web apps. This makes it easy for data scientists to:
- plug ML code in PyTorch, Tensorflow etc.
- perform computations and aggregations in Pandas
- display images created using Matplotlib / Seaborn etc.

Doccano uses a SQL-database to store data. By default it works with SQLite, but for serious applications we recommend Postgres. The docker version of Doccano includes a Posgres server set. If you choose to install Doccano yourself, you should also install Posgres.

Doccano also uses Vue.js, which offers simple & powerful templating of HTML pages. This means you can easily add your own project types for annotation of specific tasks.

## Installation and Deployment
See [this page](INSTALLATION.md).

## Usage
See [this page](usage.md).

### Tutorial

We prepared a NER annotation tutorial, which can help you have a better understanding of doccano. Please first read the README page, and then take the tutorial. [A Tutorial For Sequence Labeling Project](https://github.com/gong-io/doccano/wiki/A-Tutorial-For-Sequence-Labeling-Project).

I hope you are having a great day!

## Contribution

Doccano is under continuous development, in both [the original project](https://github.com/chakki-works/doccano) and this fork made by Gong.io. As a mature company that works at scale, we at [Gong.io](https://gong.io) developed many features on top of the original project, to support scalability, better maintanence and faster annotation. We continue active development according to our needs and issues and requests arising from the open-source community at this fork.

If you have requests for features, please file an issue describing your request. Also, if you want to see work towards a specific feature, feel free to contribute by working towards it. The standard procedure is to fork the repository, add a feature, fix a bug, then file a pull request that your changes are to be merged into the main repository and included in the next release.

Here are some tips that might help - [How to Contribute to the Doccano Project](https://github.com/chakki-works/doccano/wiki/How-to-Contribute-to-Doccano-Project)


## Contact

For help and feedback, please feel free to contact [the original author](https://github.com/Hironsan) or [the team at Gong.io](https://github.com/gong-io) that contributes to this fork.
