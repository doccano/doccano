# Get started with doccano

## What is doccano?

**doccano** is an open-source data labeling tool for machine learning practitioners. You can use doccano to perform different types of labeling tasks with many data formats. To see what doccano can do, try the [doccano demo](http://doccano.herokuapp.com).

![Demo image](https://raw.githubusercontent.com/doccano/doccano/master/docs/images/demo/demo.gif)

You can also integrate doccano with your script via the doccano REST APIs. By using the doccano APIs, you can label your data by using some machine learning model.

## Doccano labeling workflow

To complete a labeling project with doccano:

1. Install doccano.
2. Run doccano.
3. Set up the labeling project. Select the type of labeling project and configure project settings.
4. Import your dataset. You can also import labeled datasets.
5. Add users to the project.
6. Define the annotation guideline.
7. Start labeling the data.
8. Export the labeled dataset.

## Quickstart

1. Install doccano with pip (Python 3.8+):

      ```bash
      pip install doccano
      ```

2. Run doccano:

         doccano init
         doccano createuser
         doccano webserver
         # In another terminal, run the command:
         doccano task

3. Open the doccano UI at <http://localhost:8000/auth>.
4. Sign in with the username and password created by `doccano createuser`.

      The default is **username:** admin, **password:** password.

5. Change the default admin password at <http://localhost:8000/admin/password_change/>.
6. Return to the doccano UI at <http://localhost:8000/projects?>. 
7. Create a project for labeling data. Click **Create**, select a project type, and fill out project details.
8. Import a dataset. Go to the **Dataset** page and click **Actions** >  **Import Dataset** and import the dataset you want to use.
9. Click **Annotate** and label the data.
10. When you're finished, export the labeled dataset. Go to the **Dataset** page and click **Actions** > **Export dataset**.

## Architecture

You can customize doccano to suit your needs. The architecture of doccano consists of two parts: backend and frontend.

|      Module      |                 Technology                  |                Description                 |
| ---------------- | ------------------------------------------- | ------------------------------------------ |
| [doccano backend](https://github.com/doccano/doccano/tree/master/backend)  | Python, [Django](https://www.djangoproject.com/), and [Django Rest Framework](https://www.django-rest-framework.org/)   | Perform data labeling via REST APIs.              |
| [doccano frontend](https://github.com/doccano/doccano/tree/master/frontend) | Javascript web app using [Vue.js](https://vuejs.org/) and [Nuxt.js](https://nuxtjs.org/) | Perform data labeling in a user interface. |

## Contact
If you get stuck, check the [FAQ](faq.md).

For help and feedback, feel free to contact [the author](https://github.com/Hironsan).
