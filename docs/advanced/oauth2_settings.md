This document aims to instruct how to setup OAuth for doccano. doccano now supports social login via GitHub and Active Directory by [#75](https://github.com/chakki-works/doccano/pull/75). In this document, we show GitHub OAuth as an example. 


## Create OAuth App

1. In the upper-right corner of GitHub, click your profile photo, then click **Settings**.
2. In the left sidebar, click **Developer settings**.
3. In the left sidebar, click **OAuth Apps**.
4. Click **New OAuth App**.
5. In "Application name", type the name of your app.
6. In "Homepage URL", type the full URL to your app's website.
7. In "Authorization callback URL", type the callback URL(e.g. <https://example.com/social/complete/github/>) of your app.
8. Click Register application.

## Set enviromental variables

Once the application is registered, your app's `Client ID` and `Client Secret` will be displayed on the following page:
![image](https://user-images.githubusercontent.com/6737785/51811605-1073d480-22f1-11e9-8be0-726a8ee5e832.png)

1. Copy the `Client ID` and `Client Secret` from the Developer Applications of your app on GitHub.
2. Set the `Client ID` and `Client Secret` to enviromental variables:

```bash
export OAUTH_GITHUB_KEY=YOUR_CLIENT_ID
export OAUTH_GITHUB_SECRET=YOUR_CLIENT_SECRET
```

## Run server

```bash
python manage.py runserver
```

Go to login page:

![image](https://user-images.githubusercontent.com/6737785/51812454-e7edd980-22f4-11e9-80c6-2f18fbc49108.png)