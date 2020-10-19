# FastAPI-Djando
Using FastAPI with Django
# Create a project and define an engineering data model
python manage.py startproject goatfish  
python manage.py startapp main
# Introduction
## The code  
Without further delay, the part you’ve all been waiting for, the code. This section includes both the bare essentials for getting the integration working, and some best practices I’ve found when working with FastAPI, such as URL reversing, easier DB model to API model conversion, etc. I hope you’ll find it useful.
Starting out
To begin, install FastAPI, Uvicorn and Django and create a Django project as you normally would. I recommend my “new project” template, it contains various niceties you may want to use. We’re going to replace some parts and add others. I’ve created a project called goatfish and an app called main to illustrate, you can call yours whatever you want. Make sure you add "main" to Django’s INSTALLED_APPS list in the settings so it discovers the models and migrations.
## The models  
We should probably start with our data model so everything else makes sense. The API is going to be a straightforward CRUD API, which will serve a model we’ll call Simulation and provide authentication.  
Since we have an API and a database, and the models for the two are neither semantically nor functionally identical, we’ll have two sections in our models.py, one for each model type.
## The entry point
To serve requests, we need a place for our wsgi app to live. The best place is, naturally, wsgi.py:  
This will allow Uvicorn to load and serve our app. Keep in mind that app is FastAPI’s entry point and application is Django’s. You’ll need to remember that if you deploy them to something that needs to load the WSGI entry points.
You can start the server by running uvicorn goatfish.wsgi:app --reload, but it’ll probably crash at this point because there are no URL routes yet. Let’s add them.  
## The routes
I prefer the Django convention of having each app’s route in a urls.py in the app directory, so let’s put them there:
## The views
The views are more straightforward than you’d expect. We have the GET/POST on the collection and GET/POST/PUT/DELETE on the object, but the heavy lifting is done by the from_model/from_api methods.
Also, notice how authentication is done with the Depends(get_user) dependency, making it mandatory for each endpoint, and the simulation parameter is an actual Simulation model instance, not an ID. The model instance also gets validated to make sure it actually belongs to the user. We’ll see exactly how in a later section.
## Utils
In this file we define methods to authenticate users and retrieve objects from the database by their ID while still making sure they belong to the authenticating user. get_object is a generic function to avoid repeating ourselves for every one of our models.
## Tests
The tests are very close to what you’re already used to from Django. We’ll be using Django’s testing harness/runner, but we can test FastAPI’s views by using FastAPI’s client. We’ll also be using Django’s/unittest’s assert functions, as I find them more convenient, but you can use anything you’d use with Django for those.
As I mentioned earlier, the plain TestCase didn’t work for me, so I had to use the TransactionTestCase.
## Be careful
You need to use this custom runner, otherwise PostgreSQL connections don’t get cleaned up, for some reason. I’d love to figure out why, but after hours of debugging I didn’t manage to get anywhere, so I added this workaround.
You need to add TEST_RUNNER = "main.TestRunner" to your settings.py to use that.
## Last wishes
I hope that was clear enough, there is a bit of confusion when trying to figure out which part is served by which library, but I’m confident that you’ll be able to figure it all out without much difficulty. Just keep in mind that FastAPI does everything view-specific and Django does everything else.
I was legitimately surprised at how well the two libraries worked together, and how minimal the amounts of hackery involved were. I don’t really see myself using anything else for APIs in the future, as the convenience of using both libraries is hard to beat. I hope that asynchronicity will work when Django releases async support, which would complete this integration and give us the best of both worlds.
