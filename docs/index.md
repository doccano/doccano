# Get started with doccano

## What is doccano?

doccano is an open-source data labeling tool for machine learning practitioners. You can perform different types of labeling tasks with many data formats. You can try doccano from the [demo page](http://doccano.herokuapp.com).

![Demo image](https://raw.githubusercontent.com/doccano/doccano/master/docs/images/demo/demo.gif)

You can also integrate doccano with your script because it exposes the features as REST APIs. By using the APIs, you can label your data by using some machine learning model. See API documentation in detail.

## Labeling workflow with doccano

Start and finish a labeling project with doccano by the following steps:

1. Install doccano.
2. Run doccano.
3. Set up the labeling project. Select the type of labeling project and configure project settings.
4. Import dataset. You can also import labeled datasets.
5. Add users to the project.
6. Define the annotation guideline.
7. Start labeling the data.
8. Export the labeled dataset.

## Quick start

1. Install doccano:

```bash
pip install doccano
```

2. Run doccano:

```bash
doccano init
doccano createuser
doccano webserver
# In another terminal, run the following command:
doccano task
```

3. Open doccano UI at <http://localhost:8000>.
4. Sign up with a username and password created by the `doccano createuser`.
5. Click `Create` to create a project and start labeling data.
6. Click `Import dataset` on the dataset page and import the dataset you want to use.
7. Click `Start annotation` and label the data.
8. Click `Export dataset` on the dataset page and export the labeled dataset.

## Architecture

You can customize doccano to suit your needs. The architecture of doccano consists of two parts: backend and frontend.

|      Module      |                 Technology                  |                Description                 |
| ---------------- | ------------------------------------------- | ------------------------------------------ |
| [doccano backend](https://github.com/doccano/doccano/tree/master/backend)  | Python, [Django](https://www.djangoproject.com/), and [Django Rest Framework](https://www.django-rest-framework.org/)   | Perform data labeling via REST APIs.              |
| [doccano frontend](https://github.com/doccano/doccano/tree/master/frontend) | Javascript web app using [Vue.js](https://vuejs.org/) and [Nuxt.js](https://nuxtjs.org/) | Perform data labeling in a user interface. |

## Contact

For help and feedback, please feel free to contact [the author](https://github.com/Hironsan).
