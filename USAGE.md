## Usage

### Start the development server

First, start the development server. Depending on your installation method, there are two options:

**Option 1: Running the Docker image as a Container**

First, run a Docker container:

```bash
docker run -d --name doccano -p 8080:80 chakkiworks/doccano
```

Then, execute `create-admin.sh` script for creating a superuser.

```bash
docker exec doccano tools/create-admin.sh "admin" "admin@example.com" "password"
```

**Option 2: Running Django development server**
Under the `app/` folder, run:

```bash
python manage.py runserver
```

Now, open a Web browser and go to <http://127.0.0.1:8080/login/>. You should see the login screen:

<img src="./docs/login_form.png" alt="Login Form" width=400>

### Create a project

Now, try logging in with the superuser account you created in the previous step. You should see the doccano projects list page:

<img src="./docs/projects.png" alt="projects" width=600>

On first login, there is no project created yet. To create your project, make sure you’re in the project list page and click the `Create Project` button. You should see the following screen:

<img src="./docs/create_project.png" alt="Project Creation" width=400>

In this step, you can select from one of the available project types: 
- text classificatioin
- sequence labeling
- sequence to sequence
- image classification
- image labeling
- audio classification

You should select the type of project that best suits your needs. You can't change the project type later.

### Import Data

After creating a project, click `Import Data` in the navigation bar. You should see the following screen:

<img src="./docs/upload.png" alt="Upload project" width=600>

You can upload two types of files:
- `CSV file`: The first row of the file must contain the column headers, and one of them should be a `text` column. Alternatively, the file should have a single-column CSV file. If the file has multiple columns, columns that are not `text` would be uploaded as metadata, allowing you to query records according to them later.
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

Any other columns (for csv) or keys (for json) are preserved and will be exported in the `metadata` column or key as is.

Once you select a TXT/JSON file on your computer, click `Upload dataset` button. After uploading the dataset file, we will see the `Dataset` page (or click `Dataset` button list in the left bar). This page displays all the documents we uploaded in one project.

### Define labels

Click the `Labels` button in left bar to set your own labels. Note that in the text classification project type, each record can be assigned with multiple labels. 
You should see the label editor page. In label editor page, you can create labels by specifying the label text, shortcut key, background color and text color.  
You can edit existing labels by clicking on them. 

<img src="./docs/label_editor.png" alt="Edit label" width=600>

### Annotation

Now, you are ready to annotate the data. Click the `Annotate Data` button in the navigation bar, and start annotating.  
Annotations are saved along with the annotating user id and the time of the annotation.  
Multiple users can annotate the same record, leading to higher confidence in the correctness of the human labels when labels match.  
We recommend to pay special attention to cases where the annotations of different human labelers don't match. These are often hard cases, where better guidelines should be provided. 
These cases might require a new class, and it might be "okay" for your ML model to be "wrong" about these. 

<img src="./docs/annotation.png" alt="Edit label" width=600>

### Active Learning

When you click `Run model` in the top navigation bar, a Machine Learning model runs in the background, predicting the label+score of all documents based on existing human labels.
Once a model was trained, you can turn on the `Explain mode` in the annotation screen. This will highlight words that contribute to one of the set labels:
[[TODO: Add screenshot of the explain mode]]

In the `project settings` page, available through the left panel, you can choose to sort documents for labeling according to the confidence the model has in their label, so that documents with low confidence (that tend to have a larger impact on model performance) are labeled first by labelers.  
Additionally, under `project settings` you can also set to show the predicted class and model confidnce for each record, for faster labeling.

### Export Data

After the annotation step, you can download the annotated data. Click the `Edit data` button in navigation bar, and then click `Export Data`. You should see below screen:

<img src="./docs/export_data.png" alt="Edit label" width=600>

You can export data as CSV file or JSON file by clicking the button. As for the export file format, you can check it here: [Export File Formats](https://github.com/gong-io/doccano/wiki/Export-File-Formats). 

Each exported document will have metadata column or key, which will contain
additional columns or keys from the imported document. The primary use-case for metadata is to allow you to match exported data with other system
by adding `external_id` to the imported file. For example:

Input file may look like this:
`import.json`
```JSON
{"text": "EU rejects German call to boycott British lamb.", "external_id": 1}
```
and the exported file will look like this:
`output.json`
```JSON
{"doc_id": 2023, "text": "EU rejects German call to boycott British lamb.", "labels": ["news"], "username": "root", "metadata": {"external_id": 1}}
```
