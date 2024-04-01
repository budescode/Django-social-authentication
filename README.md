# Django social auth

## Introduction
Social media authentication is an added advantage to your web application because your users do not have to go through the hassle of filling forms in creating account by inputting their username, email, passwords etc. 
They just have to select the social media of their choice and signin.

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/budescode/Django-social-authentication.git
$ cd Django-social-authentication
```

## Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv myenv
$ source myenv/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

## Create a .env file in the project filder and add the following details. The right credentials should be used

```
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_SECRET=your_facebook_secret
FACEBOOK_REDIRECT_URL=http://yourredirecturl.com
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URL=http://yourredirecturl.com
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URL=http://yourredirecturl.com
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URL=http://yourredirecturl.com
```

Once `pip` has finished downloading the dependencies:
```sh

(env)$ python manage.py runserver


