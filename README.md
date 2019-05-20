# Doccano - Effective annotation of text, image and audio using Active Learning and Guided Search

[![Build Status](https://travis-ci.org/chakki-works/doccano.svg?branch=master)](https://travis-ci.org/chakki-works/doccano)

Creating high-quality labels for a proprietary dataset is challenging, time consuming and expensive. Doccano is an open-source platform for the classification of text, images and audio that significantly reduces the time it takes to train machine learning models on real datasets by integrating Active Learning and Guided Search.

Doccano provides annotation features for text classification, sequence labeling, sequence to sequence, image classification, image labeling and audio classification, and can be easily extended to new types of annotation tasks. Using Doccano, you can create labeled data for sentiment analysis, named entity recognition, text summarization and so on. Just create a new project, upload your data and start annotating.

Doccano prompts labelers to annotate examples that would most likely improve model performance, leading to a significant reduction in the number of labeled examples required. Keyword search is available for text documents, leading to faster generation of annotated datasets that are expanded by machine learning algorithms even for highly imbalanced datasets.

Doccano allows for the integration of the work of multiple labelers, and provides administrative tools to for evaluating the performance of each labeler as well as inter-labeler agreement. It further combines the labelers annotations to create a joint gold standard.

## Presentation
We presented Doccano at the <a target="_blank" href="https://www.aidatasciencesummit.com/">2019 Data Science Summit</a>. Slides are available <a target="_blank" href="https://docs.google.com/presentation/d/12T0AzfMb_0ikfxP4ZA2eaGaVyx9w45PoFKC6oSF2dVU/edit?usp=sharing">here</a>.

## Features

* Provides collaborative annotation of multiple labelers, with user authentication
* Language independent
* Fits a wide variety of project types, and can be easily extended
* Supports annotation of large datasets (1M records)
* Includes admin reports about labels and labelers
  * View each labeler’s performance on ground truth
  * Retrain low-performing labelers
  * Identify unclear guidelines
  * Calculate inter-rater agreement (loosely associated with a limit to model performance)
  * Compute the labeling speed of each labeler
  * Estimate effort required to create a certain dataset size
* Fast creation of training datasets, using:
  * Active learning - a Machine Learning model is trained based on existing annotations. Labelers are then served records with low model confidence first, and can view the predicted class for faster affirmation/rejection.
  * Guided search - filter results by matching text (e.g. a search for `"i will share" –screen` will return only documents with exact match of "i will share" and without the word "screen"). This allows fast labeling of documents with very high probability of belonging to a certain class.
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

## Installation, Deployment and Tests
See [this page](INSTALLATION.md).

## Usage
See [this page](usage.md).

## Use Cases

### [Sentiment analysis](https://doccano.herokuapp.com/demo/text-classification/)

This demo is a text classification task. Since there may be more than one label per document, you can use multiple labels when annotating.

![Text Classification](./docs/text_classification.gif)

### [Named entity recognition](https://doccano.herokuapp.com/demo/named-entity-recognition/)

In named-entity recognition projects you mark part of the text and annotate it as one of the available labels. A common use case is annotating people, places, company names etc. in text documents.

![Named Entity Recognition](./docs/named_entity_annotation.gif)

### [Sequence to Sequence & Machine translation](https://doccano.herokuapp.com/demo/translation/)

In Sequence-to-sequence (aka seq2seq) models you provide text that matches the original text. A common use case is machine translation - you are given a sentence in French, and need to translate it to English. Since there may be more than one responses in sequence to sequence tasks, you can create multi responses.

![Machine Translation](./docs/translation.gif)

## Contribution
See [this page](CONTRIBUTING.md).

## Contact

For help and feedback, please feel free to contact [the original author](https://github.com/Hironsan) or [the team at Gong.io](https://github.com/gong-io) that contributes to this fork.
