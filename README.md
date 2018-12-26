# doccano

doccano is an open source text annotation tool for human. It provides annotation features for text classification, sequence labeling and sequence to sequence. So, you can create labeled data for sentiment analysis, named entity recognition, text summarization and so on. Just create project, upload data and start annotation. You can build dataset in hours.

## Demo

You can enjoy [annotation demo](http://doccano.herokuapp.com).

### [Named entity recognition](https://doccano.herokuapp.com/demo/named-entity-recognition/)

First demo is one of the sequence labeling tasks, named-entity recognition. You just select text spans and annotate it. Since doccano supports shortcut key, so you can quickly annotate text spans.

![Named Entity Recognition](./docs/named_entity_annotation.gif)

### [Sentiment analysis](https://doccano.herokuapp.com/demo/text-classification/)

Second demo is one of the text classification tasks, topic classification. Since there may be more than one category, you can annotate multi-labels.

![Text Classification](./docs/text_classification.gif)

### [Machine translation](https://doccano.herokuapp.com/demo/translation/)

Final demo is one of the sequence to sequence tasks, machine translation. Since there may be more than one responses in sequence to sequence tasks, you can create multi responses.

![Machine Translation](./docs/translation.gif)

## Features

* Collaborative annotation
* Language independent
* (future) Auto labeling

## Requirements

* Python 3.6+
* django 2.0.5+
* Google Chrome(highly recommended)

## Installation

To install doccano, simply run:

```bash
$ git clone https://github.com/chakki-works/doccano.git
$ cd doccano
$ pip install -r requirements.txt
$ cd app
```

First we need to make migration. Run the following command:

```bash
$ python manage.py migrate
```

Next we need to create a user who can login to the admin site. Run the following command:


```bash
$ python manage.py createsuperuser
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

## Usage

### Start the development server

Let’s start the development server and explore it.

If the server is not running start it like so:

```bash
$ python manage.py runserver
```

Now, open a Web browser and go to <http://127.0.0.1:8080/login/>. You should see the login screen:

<img src="./docs/login_form.png" alt="Login Form" width=400>

### Create a project

Now, try logging in with the superuser account you created in the previous step. You should see the doccano project list page:

<img src="./docs/projects.png" alt="projects" width=600>

There is no project created yet. Here we take an NER annotation task for science fictions to give you a brief tutorial on doccano.

Below is a JSON file containing lots of science fictions description with different languages.

`books.json`
```JSON
{"text": "The Hitchhiker's Guide to the Galaxy (sometimes referred to as HG2G, HHGTTGor H2G2) is a comedy science fiction series created by Douglas Adams. Originally a radio comedy broadcast on BBC Radio 4 in 1978, it was later adapted to other formats, including stage shows, novels, comic books, a 1981 TV series, a 1984 video game, and 2005 feature film."}
{"text": "《三体》是中国大陆作家刘慈欣于2006年5月至12月在《科幻世界》杂志上连载的一部长篇科幻小说，出版后成为中国大陆最畅销的科幻长篇小说之一。2008年，该书的单行本由重庆出版社出版。本书是三体系列（系列原名为：地球往事三部曲）的第一部，该系列的第二部《三体II：黑暗森林》已经于2008年5月出版。2010年11月，第三部《三体III：死神永生》出版发行。 2011年，“地球往事三部曲”在台湾陆续出版。小说的英文版获得美国科幻奇幻作家协会2014年度“星云奖”提名，并荣获2015年雨果奖最佳小说奖。"}
{"text": "『銀河英雄伝説』（ぎんがえいゆうでんせつ）は、田中芳樹によるSF小説。また、これを原作とするアニメ、漫画、コンピュータゲーム、朗読、オーディオブック等の関連作品。略称は『銀英伝』（ぎんえいでん）。原作は累計発行部数が1500万部を超えるベストセラー小説である。1982年から2009年6月までに複数の版で刊行され、発行部数を伸ばし続けている。"}
```

To create your project, make sure you’re in the project list page and select `Create Project` button. You should see the following screen:

<img src="./docs/create_project.png" alt="Project Creation" width=400>

In this step, you can select three project types: text classificatioin, sequence labeling and sequence to sequence. You should select a type with your purpose.

As for the tutorial, we name the project as `sequence labeling for books`, write some description, choose sequence labeling project type and select the user we created.

### Import Data

After creating a project, you will see the "Import Data" page, or click `Import Data` button in the navigation bar. You should see the following screen:

<img src="./docs/upload.png" alt="Upload project" width=600>

You can upload two types of files:
- `TXT file`: each line contains a text and no line breaks (`\n`).
- `JSON file`: each line contains a JSON object with a `text` key. JSON format supports line breaks rendering.

> Notice: Doccano won't render line breaks in annotation page for sequence labeling task due to the indent problem, but the exported JSON file still contains line breaks.

`example.txt` (or `example.csv`)
```python
EU rejects German call to boycott British lamb.
President Obama is speaking at the White House.
He lives in Newark, Ohio.
...
```
`example.json`
```JSON
{"text": "EU rejects German call to boycott British lamb."}
{"text": "President Obama is speaking at the White House."}
{"text": "He lives in Newark, Ohio."}
...
```

Once you select a TXT/JSON file on your computer, click `Upload dataset` button. As for the tutorial, we select JSON format and upload the `books.json` file.

After uploading the dataset file, we will see the `Dataset` page (or click `Dataset` button list in the left bar). This page displays all the documents we uploaded in one project.

### Define labels

Click `Labels` button in left bar to define your own labels. You should see the label editor page. In label editor page, you can create labels by specifying label text, shortcut key, background color and text color.

<img src="./docs/label_editor.png" alt="Edit label" width=600>

As for the tutorial, we created some entities related to science fictions.

### Annotation

Now, you are ready to annotate the texts. Just click the `Annotate Data` button in the navigation bar, you can start to annotate the documents you uploaded.

<img src="./docs/annotation.png" alt="Edit label" width=600>

### Export Data

After the annotation step, you can download the annotated data. Click the `Edit data` button in navigation bar, and then click `Export Data`. You should see below screen:

<img src="./docs/export_data.png" alt="Edit label" width=600>

You can export data as CSV file or JSON file by clicking the button. Below is the annotated result for our tutorial project.

`sequence_labeling_for_books.json`
```JSON
{"doc_id": 33, "text": "The Hitchhiker's Guide to the Galaxy (sometimes referred to as HG2G, HHGTTGor H2G2) is a comedy science fiction series created by Douglas Adams. Originally a radio comedy broadcast on BBC Radio 4 in 1978, it was later adapted to other formats, including stage shows, novels, comic books, a 1981 TV series, a 1984 video game, and 2005 feature film.", "entities": [[0, 36, "Title"], [63, 67, "Title"], [69, 75, "Title"], [78, 82, "Title"], [89, 111, "Genre"], [130, 143, "Person"], [158, 180, "Genre"], [184, 193, "Other"], [199, 203, "Date"], [254, 265, "Genre"], [267, 273, "Genre"], [275, 286, "Genre"], [290, 294, "Date"], [295, 304, "Genre"], [308, 312, "Date"], [313, 323, "Genre"], [329, 333, "Date"], [334, 346, "Genre"]], "username": "admin"}
{"doc_id": 34, "text": "《三体》是中国大陆作家刘慈欣于2006年5月至12月在《科幻世界》杂志上连载的一部长篇科幻小说，出版后成为中国大陆最畅销的科幻长篇小说之一。2008年，该书的单行本由重庆出版社出版。本书是三体系列（系列原名为：地球往事三部曲）的第一部，该系列的第二部《三体II：黑暗森林》已经于2008年5月出版。2010年11月，第三部《三体III：死神永生》出版发行。 2011年，“地球往事三部曲”在台湾陆续出版。小说的英文版获得美国科幻奇幻作家协会2014年度“星云奖”提名，并荣获2015年雨果奖最佳小说奖。", "entities": [[1, 3, "Title"], [5, 7, "Location"], [11, 14, "Person"], [15, 22, "Date"], [23, 26, "Date"], [28, 32, "Other"], [43, 45, "Genre"], [53, 55, "Location"], [70, 75, "Date"], [126, 135, "Title"], [139, 146, "Date"], [149, 157, "Date"], [162, 172, "Title"], [179, 184, "Date"], [195, 197, "Location"], [210, 212, "Location"], [227, 230, "Other"], [220, 225, "Date"], [237, 242, "Date"], [242, 245, "Other"]], "username": "admin"}
{"doc_id": 35, "text": "『銀河英雄伝説』（ぎんがえいゆうでんせつ）は、田中芳樹によるSF小説。また、これを原作とするアニメ、漫画、コンピュータゲーム、朗読、オーディオブック等の関連作品。略称は『銀英伝』（ぎんえいでん）。原作は累計発行部数が1500万部を超えるベストセラー小説である。1982年から2009年6月までに複数の版で刊行され、発行部数を伸ばし続けている。", "entities": [[1, 7, "Title"], [23, 27, "Person"], [30, 34, "Genre"], [46, 49, "Genre"], [50, 52, "Genre"], [53, 62, "Genre"], [63, 65, "Genre"], [66, 74, "Genre"], [85, 88, "Title"], [9, 20, "Title"], [90, 96, "Title"], [108, 114, "Other"], [118, 126, "Other"], [130, 135, "Date"], [137, 144, "Date"]], "username": "admin"}
```

Congratulation! You just mastered how to use doccano for a sequence labeling project. As for the export data of document classification and sequence to sequence, you can check it below.

**JSON output**

The export json format: every annotated document will be a one line, and each line will be a python dictionary class with 4 keys.
* `doc_id`: document id
* `text`: original text
* `labels/entities/sentences`: annotation
* `username`: annotater name

A json export example for *document classification*.
```JSON
{"doc_id": 20, "text": "Barack Hussein Obama II is an American politician \nwho served as the 44th President of the United States from January 20, 2009, to January 20, 2017.", "labels": ["label1"], "username": "admin"}
{"doc_id": 21, "text": "贝拉克·侯赛因·奥巴马是一个美国的政治家，曾担任第四十四任美国总统，\n任期从2009月1月20日到2017年1月20。", "labels": ["label1", "label2"], "username": "admin"}
{"doc_id": 22, "text": "バラク・フセイン・オバマ2世は、アメリカの政治家であり、\n2009年1月20日から2017年1月20日まで、第44代米国大統領を務めた。", "labels": ["label1", "label2", "label3"], "username": "admin"}
```

A json export example for *sequence labeling*. The position of entity will ignore line breaks.
```JSON
{"doc_id": 23, "text": "Barack Hussein Obama II is an American politician \nwho served as the 44th President of the United States from January 20, 2009, to January 20, 2017.", "entities": [[0, 20, "PER"], [87, 104, "ORG"], [110, 126, "DATE"], [131, 147, "DATE"]], "username": "admin"}
{"doc_id": 24, "text": "贝拉克·侯赛因·奥巴马是一个美国的政治家，曾担任第四十四任美国总统，\n任期从2009月1月20日到2017年1月20。", "entities": [[0, 11, "PER"], [29, 31, "ORG"], [38, 48, "DATE"], [49, 58, "DATE"]], "username": "admin"}
{"doc_id": 25, "text": "バラク・フセイン・オバマ2世は、アメリカの政治家であり、\n2009年1月20日から2017年1月20日まで、第44代米国大統領を務めた。", "entities": [[0, 12, "PER"], [16, 20, "ORG"], [29, 39, "DATE"], [41, 51, "DATE"]], "username": "admin"}
```

A json export example for *sequence to sequence*.
```JSON
{"doc_id": 26, "text": "Barack Hussein Obama II is an American politician \nwho served as the 44th President of the United States from January 20, 2009, to January 20, 2017.", "sentences": ["バラク・フセイン・オバマ2世は、アメリカの政治家であり、  2009年1月20日から2017年1月20日まで、第44代米国大統領を務めた。"], "username": "admin"}
{"doc_id": 27, "text": "贝拉克·侯赛因·奥巴马是一个美国的政治家，曾担任第四十四任美国总统，\n任期从2009月1月20日到2017年1月20。", "sentences": ["Barack Hussein Obama II is an American politician  who served as the 44th President of the United States from January 20, 2009, to January 20, 2017.", "贝拉克·侯赛因·奥巴马是一个美国的政治家，曾担任第四十四任美国总统， 任期从2009月1月20日到2017年1月20。"], "username": "admin"}
{"doc_id": 28, "text": "バラク・フセイン・オバマ2世は、アメリカの政治家であり、\n2009年1月20日から2017年1月20日まで、第44代米国大統領を務めた。", "sentences": ["Barack Hussein Obama II is an American politician  who served as the 44th President of the United States from January 20, 2009, to January 20, 2017."], "username": "admin"}
```

Because we save each JSON obejct as one line in the JSON file, you should read it line by line. Here is a simple script to load such format for your task.

```Python
import json
with open("export.json") as f:
    jsons = [json.loads(line) for line in f]
```

**CSV output**

The CSV export format for *document classification* has four columns: document id, text, label (one label a line), user name. Below is a multi-label example.

```CSV
20,"Barack Hussein Obama II is an American politician who served as the 44th President of the United States from January 20, 2009, to January 20, 2017.",label1,admin
20,"Barack Hussein Obama II is an American politician who served as the 44th President of the United States from January 20, 2009, to January 20, 2017.",label2,admin
20,"Barack Hussein Obama II is an American politician who served as the 44th President of the United States from January 20, 2009, to January 20, 2017.",label3,admin
...
```

The CSV export format for *sequence labeling* is the [IOB format](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging) in a character-level, which has three columns: document id, character, entity.

```CSV
23,B,B-PER
23,a,I-PER
23,r,I-PER
23,a,I-PER
23,c,I-PER
23,k,I-PER
23, ,I-PER
23,H,I-PER
23,u,I-PER
23,s,I-PER
23,s,I-PER
23,e,I-PER
23,i,I-PER
23,n,I-PER
23, ,I-PER
23,O,I-PER
23,b,I-PER
23,a,I-PER
23,m,I-PER
23,a,I-PER
23, ,O
23,I,O
23,I,O
23, ,O
23,i,O
23,s,O
...
```

The CSV export format for *sequence to sequence* has four columns: document id, original text, sentence (one sentence a line), user name. Below example shows that the English text is translated to Chinese and Japanese.  

```CSV
26,"Barack Hussein Obama II is an American politician who served as the 44th President of the United States from January 20, 2009, to January 20, 2017.",バラク・フセイン・オバマ2世は、アメリカの政治家であり、2009年1月20日から2017年1月20日まで、第44代米国大統領を務めた。,admin
26,"Barack Hussein Obama II is an American politician who served as the 44th President of the United States from January 20, 2009, to January 20, 2017.",贝拉克·侯赛因·奥巴马是一个美国的政治家，曾担任第四十四任美国总统， 任期从2009月1月20日到2017年1月20。,admin
```

I hope you are having a great day!

## Contribution

As with any software, doccano is under continuous development. If you have requests for features, please file an issue describing your request. Also, if you want to see work towards a specific feature, feel free to contribute by working towards it. The standard procedure is to fork the repository, add a feature, fix a bug, then file a pull request that your changes are to be merged into the main repository and included in the next release.

## Contact

For help and feedback, please feel free to contact [the author](https://github.com/Hironsan).

**If you are favorite to doccano, please follow my [GitHub](https://github.com/Hironsan) and [Twitter](https://twitter.com/Hironsan13) account.**
