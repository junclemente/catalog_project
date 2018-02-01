# Catalog Project
## Project for Fullstack Web Development at Udacity.com

This project uses a variety of technologies learned throughout the Fullstack Web Development (FSND) Nanodegree program at [Udacity.com](http://udacity.com "Udacity.com").

The application shows a list of categories which have items within the categories. All categories and items can be viewed by any user. Categories and Items can be added and edited but one must be logged in to the site. Logging in is handled by OAuth authentication through one's Google account. Once logged in to the site, users can add, edit, and delete categories and/or items that they solely created. Logged in users who are not the creater/owner will not be given the option to edit or delete. Deleting a category that contains item(s) will also provide a warning that items within that category will also be recursively deleted.

### How To Use This Page

#### Files Needed
This app uses the Google OAuth2 API to facilitate creating login credentials.
You will also need to create OAuth keys from Google. Once created, download Client ID for Web Application
as a JSON file and save it as: `/catalog/client_secrets.json`.

**Optional**  Open up the `create_db.py` file and edit the variable `TEST_USER_EMAIL_2` with your gmail address. This step is optional. If this is not done, the database will be populated with items that will not be owned by the user.

* Clone the files onto your harddrive.
* Ensure that [Vagrant](https://www.vagrantup.com/docs/installation/) is installed.
* Open an terminal window.
* Go to the `/catalog_project/vagrant` folder and type `vagrant up`. Then `vagrant ssh`.
* After ssh-ing to the vagrant box, go to `/vagrant/catalog`.
* The Vagrant file includes almost all the files required to run this application.
* On the command line, type `pip freeze -r requirements.txt` to install other dependencies for this application. (This includes Flask-WTF v0.14.2 and WTForms v2.1)
* Create and populate the test database by typing `python create_db.py`.
* Once installed, type `python application.py` to run the app.
* Open a browser and type: `localhost:8000`

#### Notes
The application will contain links at the bottom that are for test purposes only. These can be removed by editing the "base.html" template file and removing the `{% include "test.html" %}` line.

**API Endpoints** are links to the available API endpoints.

**Authenticate / Authorization Test** are for testing editing and deleting information in the database.
If `TEST_USER_EMAIL_2` in create_db.py was edited with a gmail account the user can log in to, the links will work as is. If it was not edited, then the links will not work as described. This was implemented because I was not able to implement the flaskr unittesting [Testing Flask Applications](http://flask.pocoo.org/docs/0.12/testing/ "Testing Flask Applications")

#### JSON Endpoints

There are four JSON endpoints:
* List all Categories: `/api/allcategories`
* List all Items: `/api/allitems`
* List all Items in a Category (requires Category ID number): `/api/itemsincategory/<category_id>`
* List Item (requires Item ID number): `/api/item/<item_id>`


### Languages / Frameworks / Libraries / APIs
- Python 2.7
- Bootstrap 3
- CSS3
- HTML5
- Javascript
- jQuery
- Google OAuth2 API

### Resources
- Bootstrap v3 [getBoostrap.com](http://getbootstrap.com "getBootstrap.com")
- Favicon & App Icon Generator - Dan's Tools [www.favicon-generator.com](https://www.favicon-generator.org "favicon-generator.org")
