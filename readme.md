# Promo System

this is a back-end promo system in which users are assigned various promos and can use the promo points in a specific task of their choosing 

## you can do 
    * signup for normal user
    * Create_promo
        allows admin user to create a promo to a normal user
    * Modify_promo
        allows admin user to modify a promo that already exists
    * Delete_promo
        allows admin user to delete a promo that already exists
    * Get_promo_list_all_users
        allows admin user to retrieve a list of all promos that exist
    * Get_promo_list_me
        allows normal user to retrieve a list of their promos
    * Get_promo_points
        allows normal user to get the remaining points from a particular promo
    * Use_promo_points
        allows normal users to deduct some of the points from one of their promos

## Install

* you need to install python3
* you need to install pip or pip3 package
* postman or google chrome

## Run the project

* download the project 
* open the project in terminal by press `Ctrl-Alt+T`
* install virtualenv `pip install virtualenv` 
* init your virtualenv `virtualenv promo_env`
* active virtualenv `source promo_env/bin/activate`
* install required packages on virtualenv `pip install -r requirements.txt`
* migrate models to create tables in db `python manage.py migrate`
* run server `python manage.py runserver`
* use this api postman collection for using the system(https://www.getpostman.com/collections/c896b1598bf9a592a6cc)

## Run test cases

    * if you want to see some unit tests on all end points
        1.open (https://github.com/Mohamed-awad/PromoSystem/blob/master/promoApplication/api/tests.py)
    * if you want to run tests cases
        1.run this command ```python manage.py test```

## Important Notes
    * for create admins in the system
        1. you should create super by run ```python manage.py createsuperuser```
        2. login to /admin
        3. create user in users that exist in PROMOAPPLICATION
        4. when create user make is_admin checkbox checked
        
    * for use any end point in the system except (signup & login)
        1. you need to send in headers Authurization token
        2. you can get it from login end point /api/auth/login/