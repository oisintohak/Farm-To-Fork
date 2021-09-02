# [Farm-To-Fork](https://farmtofork.herokuapp.com/)

Vegetable Delivery Service

Welcome to Farm To Fork. This application was built to allow consumers to buy produce directly from farmers and for farmers to be able to sell their produce online directly to consumers. Consumers can buy products from the website without having to register for an account. Users can register for a Customer or Farmer account. Both account types can purchase products but only Farmers can add products. 

The live website can be found here: [Farm-To-Fork](https://farmtofork.herokuapp.com/).

To test the checkout process use the stripe test card details:

- Card number: 4242424242424242
- CVC: Any 3 digits
- Expiry: Any future date (eg. 04/24)

------

## User Experience Design


### Strategy

#### Site Owner Goals:

- To encourage new farmers to advertise their products on the site.
- To encourage new customers to buy products and/or subscriptions.
- To address any issues/concerns faced by either the farmers or customers.

#### User Stories

**New User**
- As a first time visitor to the site I would like to understand its' purpose.
- I would like to browse any current products offered by farmers.
- I would like to see the locations of farmers currently using the service.
- I would like to see the prices of products offered by farmers.
- I would like to understand the delivery process.

**Accounts and registration**
- I would like to register for the service as a farmer/customer.
- I would like to login/logout of the website.
- I would like to receive a confirmation email after registration.

**Finding Products**
- I would like to search for products by keyword
- I would like to sort products by name, date or distance
- I would to browse farmers and sort them by distance

**Checkout and orders**
- I would like to use a secure and user-friendly checkout
- I would like to see which products can be delivered
- I would like to receive an email confirmation after payment
- I would like to receive collection details for any products that can't be delivered
- I would like to receive a link to view my order details

**Farmers**
- I would like to see what percentage of the price paid by customers is given to farmers.
- I would like to see how often farmers are paid.
- I would like to know which payment method is used to pay farmers.
- I would like to add my details for customers to view (location, delivery range, delivery schedule, personal bio).
- I would like to add/edit/remove products.


**Customers**
- I would like to search for products.
- I would like to view info about a farmer (location, delivery range, personal bio, delivery schedule)
- I would like to filter products by distance, keyword, and rating.
- I would like to see the different sizes/prices for a product.
- I would like to pay for a product if I am located within the delivery range, or if I can collect it.
- I would like to read detailed information about the product.

### Scope

##### Planned Features:
 - The site should be responsive and user-friendly on all devices.
 - Intuitive and user-friendly navigation
 - Intuitive and user-friendly layout
 - There should be an about page that describes the purpose of the site and the delivery and farmer-fees conditions
 - The purpose of the website should be clear immediately
 - Users should be able to easily register/login/logout
 - Farmers should be able to add/edit/remove products
 - Users can search for and sort products
 - Users can search for and sort farmers
 - Users can view farmers/products on a map
 - Users can view products and add them to their cart
 - Users can enter an address to see delivery/collection information for products.
 - Users can pay for their products and receive confirmation emails with delivery/collection details
 - Farmers should receive payouts after both customer and farmer have verified the order.


 ### Structure

 #### Fulfilled User stories

**User Story:**
>  - As a first time visitor to the site I would like to understand its' purpose.

**Acceptance Criteria:**
 - The home page has a heading that clearly describes the purpose of the site and who it is for.

**Implementation:**

The home page will display a heading that clearly shows the site purpose.

-----
**User Stories:**
>  - I would like to understand the delivery process.
>  - I would like to see what percentage of the price paid by customers is given to farmers.
>  - I would like to see how often farmers are paid.
>  - I would like to know which payment method is used to pay farmers.

**Acceptance Criteria:**
 - The user can see an FAQ/About page to find the following information:
    - Details about the delivery/collection process
    - Details about farmer fees and how much of the product price is given to farmers
    - Details about how farmers are paid and how often
**Implementation:**

There is a link to an FAQ/About page in the navbar and the footer. This page will contain information about:
    - The delivery/collection process
    - Farmer fees
    - Farmer payout frequency and payout method

-----
**User Stories:**
> - I would like to browse any current products offered by farmers.
> - I would like to search for products by keyword
> - I would like to sort products by name, date or distance
> - I would like to compare the products of nearby farmers.

**Acceptance Criteria:**
 - The user can see a list of products and enter search terms to find them
 - The user can sort a list of products by name, date and distance

**Implementation:**

There is an easily accessed search icon which will show a search bar for users to enter search queries. There is also a link to 'product list' in the navbar to display a list of products. The product list has a 'sort' feature where users can sort by product name, date added and distance from the user. The distance feature will use the geolocation API to access the user's device location, or prompt them to log in and add location details to their profile.

-----
**User Stories:**
>  - I would like to see the prices of products offered by farmers.
>  - I would like to see the different sizes/prices for a product.
>  - I would like to read detailed information about the product.

**Acceptance Criteria:**
 - The user can see price information for each product on a dedicated product page
 - The user can see size information for each product on a dedicated product page
 - The user can see a detailed description of each product

**Implementation:**

There is a dedicated product page for each product that contains information about product sizes and the price for each size. There is a description section for farmers to add descriptions to products.

-----

**User Story:**
> -  I would like to see the locations of farmers currently using the service.

**Acceptance Criteria:**

- The user can access a map page to view farmer locations

**Implementation:**

There is a dedicated farmer map page where users can see farmers on a map with links to each farmer's profile and products.

-----

**User Stories:**

> - I would like to register for the service as a farmer/customer.
> - I would like to login/logout of the website.
> - I would like to receive a confirmation email after registration.

**Acceptance Criteria:**

- The user can access a registration page and enter their details
- The user receives a confirmation email after signing up
- The user can access a login page and log in.
- The user can access a logout page and log out.

**Implementation:**

There is an account icon with registration/login links displayed for unauthenticated users and a logout link displayed for authenticated users. Users will receive a confirmation email after registering.

-----

**User Story:**
> - I would like to see which products can be delivered

**Acceptance Criteria:**

- The user can view their cart and enter their address to view deliver/collection details for each product 

**Implementation:**

The user can easily access their shopping cart and proceed to checkout where they will be prompted to enter a delivery address. This address will then be used to calculate a distance for each product and determine if it is within the delivery radius. There will be an order summary displaying a delivery status for each product.

-----

**User Stories:**
>  - I would like to use a secure and user-friendly checkout
>  - I would like to receive an email confirmation after payment
>  - I would like to receive collection details for any products that can't be delivered
>  - I would like to receive a link to view my order details

**Acceptance Criteria:**

- The user can enter their card in a Stripe checkout form.
- The user receives an order confirmation email if the payment is successful.
- The user receives an email with collection details if any products are not marked for delivery.
- All emails contain a link to view the order details

**Implementation:**

The payment page features a secure stripe card checkout. If the payment is successful, a webhook handler will send the user an order confirmation email with a link to view the order details and items. If any of the products on the order require collection, the user will receive an email with the farmer contact and address information.

-----

**User Stories:**
> - As a farmer I would like to add my details for customers to view (location, personal bio).
> - As a customer would like to view info about a farmer (location, delivery range, personal bio)

**Acceptance Criteria:**

- The user can add profile information
- The user can view a profile

**Implementation:**

There is a link in the account dropdown displayed for authenticated users for 'Edit Profile'. On this page users can add information to their profiles including name, bio, image and address.

-----

**User Story:**

> - As a farmer I would like to add/edit/remove products.

**Acceptance Criteria:**

- Farmers can add new products
- Farmers can edit their
- Farmers can delete their products

**Implementation:**

There is a 'create product' link shown to authenticated farmers. On this page they can create new products. There is a 'my products' link shown to authenticated farmers. This page displays a farmer's products and on each product page there is an 'edit product' link. On the edit product page they can edit or delete the product.

-----



 #### Unfulfilled User stories

**User Story:**

> - I would to browse farmers and sort them by distance

**Acceptance Criteria:**

- The user can access a farmer list sorted by distance

**Implementation:**

There is a dedicated farmer list page where users can browse farmers and sort them by distance

##### Development plan from user stories:

As A:            | I want to be able to...         | So that I can...                                  |
-----------------| --------------------------      | ----------------------------------------          |
 Site User       | View a landing page             | Discover the purpose of the site                  |
 Farmer/Customer | Register an account             | Save my details in an account                     |
 Farmer/Customer | Login/Logout of my account      | View my account details/orders etc.               |
 Farmer/Customer | Delete my account               | Remove all of my data from the website            |
 Farmer          | Add/Edit/Remove products        | Sell my produce and keep my inventory updated     |
 Farmer/Customer | View and buy products           | Buy produce directly from local farmers           |
 Farmer/Customer | Add my location                 | Show only Products/Farmers near me                |
 Farmer/Customer | View farmers/products on a map  | Discover farmers/products in my area              |


### Wireframes


I used Balsamiq to create wireframes before building this project. During the development process some aspects of the design and layout were modified, so for some pages the result is quite different from the original design.

To view wireframes please go to the [WIREFRAMES.md](WIREFRAMES.md) file.


### Database Schema:

**Database Schema** ![Database_schema](docs/database_schema/schema.png)


### Design

##### Colors
I tried to choose a color scheme to reflect the subject matter of the website (i.e farming, nature, vegetables etc.). This led me to a combination of green and brown. I avoided using excessively vibrant colors that might negatively affect the user experience or colors that would reduce accessibility for vision impaired users. I created a [color_palette](https://material.io/resources/color/#!/?view.left=0&view.right=0&primary.color=C8E6C9&secondary.color=FFA726) with Google's Material Design Color Tool and used certain colors throughout the website. I used a light green (#fbfffc) for all page backgrounds and a green-black (#1a201a) for all text. A mint-green (#c8e6c9) was used for the navbar and footer backgrounds as well as the home-page carousels. I used a light brown (#ffd95b) for all primary action buttons and the previously mentioned light green and green black for secondary action buttons.


##### Typography
[Spectral](https://fonts.google.com/specimen/Spectral) was used for the logo and  [Roboto](https://fonts.google.com/specimen/Roboto) was used for all other text



## Technologies
- HTML
- CSS
- Bootstrap 5 for styling, layout and responsiveness.
- FontAwesome for icons
- JavaScript
    - Google Geocode API for geocoding addresses on address forms
    - jQuery django formset plugin to dynamically add/remove product variant formsets from product forms
    - leaflet.js for the farmer map page
- Python
    - Django
        - GeoDjango for storing location data
        - Django crispy forms for form styling
        - Django allauth for user authentication
        - Django countries for country fields in address forms
        - Djang-extra-views for adding formsets to modelforms
        - Django-multi-form view to display and handle multiple forms in a view
- PostgreSQL
- Amazon AWS S3 bucket for static file storage and uploads



## Testing


## Deployment

#### Local Environment
These are the steps to run this project in a local environment:
1. Install [python](https://www.python.org/downloads/) and follow the guide for your operating system [here](https://docs.python.org/3/using/)
2. install the right git command line interface for your operating system [Here](https://git-scm.com/downloads)
3. In a terminal with git installed, run ```git clone https://github.com/oisintohak/Farm-To-Fork.git``` and then ```cd Farm-To-Fork``` This will create a new directory in your default directory called 'Farm-To-Fork' and navigate into this directory.
4. Run ```pip install -r requirements.txt``` This will install all project requirements
5. Install [PostgreSQL](https://www.postgresql.org/download/)
6. Set up the requirements for GeoDjango following [this_guide](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/)
 - If you're running windows, use [this_guide](https://www.pointsnorthgis.ca/blog/geodjango-gdal-setup-windows-10/) to set up the requirements for GeoDjango
7. In your terminal create a superuser with ```python manage.py createsuperuser``` and enter the required details.
8. Make the necessary database migrations with ```python manage.py makemigrations``` ```python manage.py migrate```
9. Create a [Stripe](https://stripe.com/in) account and set up a webhook using the [stripe_documentation](https://stripe.com/docs/webhooks)
10. In the new Farm-To-Fork directory navigate to the farm_to_fork directory and create a '.env' file (this will be in the same directory as settings.py).Set the following values in your .env file
    ```
    SECRET_KEY='YOUR_DJANGO_SECRET_KEY'
    STRIPE_PUBLIC_KEY='YOUR_STRIPE_PUBLIC_KEY'
    STRIPE_SECRET_KEY='YOUR_STRIPE_SECRET_KEY'
    STRIPE_WH_SECRET='YOUR_STRIPE_WH_SECRET'
    DEBUG=1

    ```
11. Back in the terminal run the server with ```python manage.py runserver```

#### Heroku
These are the steps to deploy this project to Heroku
- Log in to Heroku
- Click 'New'
- Click 'Create New App'
- Enter an app name and choose a region
- In the 'Deployment method' section click 'connect to github'
- Choose your github repository and click Connect
- Click on the resources tab and search for postgres, select 'Heroku Postgres'
- Select hobby dev plan
- Click 'Submit Order Form'
- On the settings tab go to 'Buildpacks' and click 'Add buildpack'
- Under 'Enter buildpack URL' enter https://github.com/heroku/heroku-geo-buildpack.git
- click 'Add buildpack' again
- Add the Python buildpack
- Ensure that the https://github.com/heroku/heroku-geo-buildpack.git is above the heroku/Python buildpack
- In the settings tab click 'reveal config vars' and add the following variables
    - AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
    - EMAIL_HOST_PASS=YOUR_EMAIL_HOST_PASS
    - EMAIL_HOST_USER=YOUR_EMAIL_HOST_USER
    - SECRET_KEY=YOUR_DJANGO_SECRET_KEY
    - STRIPE_PUBLIC_KEY=YOUR_STRIPE_PUBLIC_KEY
    - STRIPE_SECRET_KEY=YOUR_STRIPE_SECRET_KEY
    - STRIPE_WH_SECRET=YOUR_STRIPE_WH_SECRET
    - USE_AWS=True
    - HEROKU=True
- In the deploy tab click 'Deploy Branch' at the bottom (with 'main' selected)
    - You can also optionally enable automatic deploys from a chosen branch, which will redeploy automatically every time you push to the branch.
- In the top right click 'More' (beside 'Open App') and select 'Run Console'
- Enter 'python manage.py migrate' and click 'Run'
- Enter 'python manage.py createsuperuser' and click 'Run'
- Enter any required details to create a superuser for the django admin
- Click 'Open App' in the top right

### Issues
 - On the product edit/create page, if 10 variants are added, the 'add variant' button disappears and doesn't come back if variants are removed.
 - Product cards do not have equal height due to differing content size.
 - Need to add, 'back to products' button on product pages.