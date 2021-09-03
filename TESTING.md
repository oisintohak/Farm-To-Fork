## Testing

### Code Validation

### Performance

## Manual Continuous Testing


This website was designed using a mobile-first approach and was tested for responsiveness on multiple device sizes in addition to browser-simulated devices in Google Chrome Developer Tools and Firefox Developer Tools

Devices Used : Redmi Note 4, Redmi Note 9, Lenovo Tab4 10

Browser device simulation:
    - Google Chrome: Moto G4, Pixel 2 XL, iPhone/SE, iPhone X, iPad, iPad Pro, Galaxy Fold
    - Mozilla Firefox: Microsoft Lumia 950 (Windows Phone 10.0), Galaxy S9/S9+ (Android 7.0), Galaxy Note 3 (Android 4.3)

The following details were verified to ensure the website was responsive and the UI and design were consistent on all devices and browser device simulations, in addition to verifying that access to certain pages was only granted to the correct users and all operations worked as expected:

- ### All pages

    ##### Visuals & Responsiveness

    - There is no horizontal overflow from any elements outside the page boundaries
    - The navbar is at the top of the page and the footer at the bottom, even if there is only a small amount of content between
    - The visuals and layout are consistent on all screen sizes

- ### Navbar

    ##### Visuals & Responsiveness

    - All links are horizontally and vertically aligned and centered
    - Dropdowns are working correctly and text can be entered into the search box
    - All link text is readable
    - If the cart total is more than 5 digits, there is no overflow and the layout is not affected negatively
    - The search input dropdown is sized correctly across all screen sizes
    - The main navigation becomes a dropdown at the appropriate screen width
    - The logo is sized appropriately at different screen widths

    ##### Functionality

    - All links work and link to the correct page
    - For the account dropdown
        - Unauthenticated users will only see the login and register links
        - Only authenticated users will see the 'my orders' 'my profile', 'edit profile' and 'logout' links
        - Only authenticated Farmers will see the 'my products' and 'create product' links

- ### Footer

    ##### Visuals & Responsiveness:

    - The logo, email, phone and about link text is readable
    - On smaller screens, only the icons are displayed for email, phone and about links
    - The logo icon is sized correctly
    - The logo icon attribution is sized correctly

    ##### Functionality:

    - All links work and link to the correct page
    - The logo attribution links open in a new tab

- ### Home

    ##### Visuals & Responsiveness:

        - Banner:
            - The banner image positioning is correct and that the apple basket is visible on all screen sizes
            - The banner text is readable and scales properly across different screen sizes
            - The banner login and register buttons are sized correctly and the text is readable

        - Carousel:
            - The carousel slide items are scaled properly across device sizes
            - The carousel doesn't display too many items for the screen width
            - The carousel item text and buttons are readable and properly aligned
            - The carousel next and previous buttons are sized properly.

    ##### Functionality:
        
        - Banner:
            - All links work and link to the right pages
        
        - Carousel:
            - All links work and link to the right pages
            - On mobile devices the carousel items can be swiped

- ### Login, Registration, Log out, Change Password Pages

    ##### Visuals & Responsiveness:

        - All text is sized correctly
        - There is adequate spacing around the text, labels, inputs and button
        - The inputs and button are size correctly
        - Any django form validation errors are sized properly and their positioning is correct

    ##### Functionality:

        - All links work and link to the right pages

    ##### Defensive design:

        - For authenticated users:
            - Navigating to the login and register pages redirects to the home page
        - For unauthenticated users:
            - Navigating the the logout page redirects to the home page
            - Navigating to the password change/reset/reset-done/set or the email confirmation/change/view email pages all redirect to the login page

- ### About Page

    ##### Visuals & Responsiveness:
  
        - All headings and paragraphs are readable
        - The sections and headings have appropriate padding and positioning

    ##### Functionality:
        
        -The login and register links are only displayed to unauthenticated users
        - If visible, the login and register links work and link to the correct pages

- ### Farmer Map
    
    ##### Visuals & Responsiveness:

        - The heading text is sized and positioned correctly
        - The map zoom and pan works as expected
        - The map markers can be clicked and the marker content is displayed properly

    ##### Functionality:

        - The farmer profile links work and link to the right pages

- ### Product List/Search Results/My Products List

    ##### Visuals & Responsiveness:

        - The product count heading and sort button text is readable
        - The sort button and dropdown menu are positioned correctly
        - The product card images are sized and positioned correctly
        - The product card text and buttons are sized and positioned correctly
        - If present, the search term display is sized and positioned correctly
        - If present, the product delivery status and distance badges are sized and positioned correctly with readable text
        - There is user feedback on the 'share location' button on the distance sorting modal that lets the user know what is happening

    ##### Functionality:

        - The sort dropdown works as expected
        - Each of the sort functions work as expected
        - All product and farmer profile links work and link to the right pages
        - On the distance sorting modal:
            - All users will see the link to share their device location
            - Only authenticated users without an address on their profile will see a link to add their address
            - Only authenticated users with an address on their profile will see a link to use their address to sort products by distance

- ##### Product Detail

    ##### Visuals & Responsiveness:

        - The product card image is sized and positioned correctly
        - The product card text and add to cart/edit product button is sized and positioned correctly
        - The variant and quantity inputs are sized and positioned correctly

    ##### Functionality:

        - All links work and link to the correct page
        - The variant select and quantity input works as expected
        - The add to cart button works as expected
    
    ##### Defensive design:

        - Authenticated farmers who have created the product will only see the 'edit product' button, all other users will only see the add to cart button

- ### Product Edit/Create Form, Product delete confirmation

    ##### Visuals & Responsiveness:

        - The heading, input and label text is sized properly
        - All elements have adequate space and are correctly aligned
        - The dynamic variant subform is displayed properly across all screen sizes
        - Any django form validation errors are sized and positioned correctly

    ##### Functionality:
        - All inputs work as expected
        - Any existing user data is in the correct fields
        - ** Unresolved Issue:**
            - The form can be saved without variants
        - ** Unresolved Issue:**
            - If a user adds 10 product variants, the 'add variant' button disappears and doesn't come back if variants are removed.
            - If 10 variants are saved and the user removes one, they will need to save the form and edit the product again to add another variant
    
    ##### Defensive design:
        - Create Product:
            - Unauthenticated users will be redirected to the login page with a message: 'Login to a farmer account to create/edit products.'
            - Users with a customer account will redirected to the home page with a message: 'Only farmer accounts can create/edit products.'
        - Edit Product:
            - Only the owner of the product can view the edit product page, all other authenticated users will be redirected to the home page with a message 'you can only edit your own products'
            - Unauthenticated users will be redirected to login with a message 'You need to login to edit your products.'
        - Delete Product:
            - Customer accounts or unauthenticated users will be redirected to the home page with a message: 'You don't have permission to delete this product.'
            - Farmers who don't own the product will be redirected to the home page with a message: 'You can only delete your own products.'

- ### Profile Detail

    ##### Visuals & Responsiveness:

        - The profile card image is sized and positioned correctly
        - The profile card text and edit profile button (if shown) is sized and positioned correctly
        - The product card images, text and 'details' button are all sized and positioned correctly

    ##### Functionality:

        - All links work and link to the correct page
        - Only the profile owner can see the edit profile button

    ##### Defensive design:

        - Unauthenticated users will be redirected to login with a message: 'Please log in to view profiles.'

- ### Profile Edit/Create Form, Profile delete confirmation

    ##### Visuals & Responsiveness:

        - The heading, input and label text is sized properly
        - All elements have adequate space and are correctly aligned
        - The button text and loading icon are displayed correctly when fetching the geocoding data on the address forms
        - Any django form validation errors are sized and positioned correctly

    ##### Functionality:
        - All inputs work as expected
        - Any existing user data is in the correct fields
        - There are validation error messages if the form is filled incorrectly
        - The submit button changes text when fetching address data and changes back when the request is completed
        - If the address can't be geo-located there is a popup modal with an error message

    ##### Defensive design:
        - Unauthenticated users will be redirected to login with a message 'Please log in to edit your profile.'

- ### Cart

    ##### Visuals & Responsiveness:

        - The headings, cart items and button text are all readable
        - The product items are spaced evenly and the buttons work as expected

    ##### Functionality:

        - All links work and link to the correct page
        - The quantity input and delete buttons work as expected
        - The update cart button works as expected

- ###  Checkout Form
    
    ##### Visuals & Responsiveness:

        - The heading, input and label text is sized properly
        - All elements have adequate space and are correctly aligned
        - The button text and loading icon are displayed correctly when fetching the geocoding data on the address forms
        - Any django form validation errors are sized and positioned correctly

    ##### Functionality:

        - All inputs work as expected
        - Any existing user data is in the correct fields
        - There are validation error messages if the form is filled incorrectly
        - The submit button changes text when fetching address data and changes back when the request is completed
        - If the address can't be geo-located there is a popup modal with an error message

    ##### Defensive design:

        - If the user has no items in their cart they are redirected to the cart page with a message 'No items in your cart.'

- ### Payment form/ Checkout complete

    ##### Visuals & Responsiveness:

        - All headings and text are sized and positioned correctly
        - All order items are sized and positioned correctly
        - The delivery information notice is positioned correctly
        - The customer details are displayed correctly
        - The card form, card validation errors, and card loading spinner are displayed correctly

    ##### Functionality:

        - Payment form:
            - Any form validation errors are displayed
            - All items have the delivery status badge displayed
            - The total is calculated correctly
        - Checkout success:
            - The users details and order number are displayed

    ##### Defensive design:

        - If the order has received the stripe success webhook, instead of trying to pay for the order again, the user will be redirected to the order detail page 

- ### Order list

    ##### Visuals & Responsiveness:

        - All headings and order titles are readable
        - There is adequate spacing around all elements

    ##### Functionality:

        - All links work and link to the correct pages

    ##### Defensive design:

        - Only display orders that have received the stripe success webhook

- ### Order detail, Farmer order detail

    ##### Visuals & Responsiveness:

        - All headings and text are sized and positioned correctly
        - All order items are sized and positioned correctly
        - The delivery information notice is positioned correctly
        - The customer details are displayed correctly

    ##### Functionality:
    
        - Any products from a specific farmer are grouped together with a deliver status badge
        - The distance is shown for each farmer
    
    ##### Defensive design:

        - If the order has not received the stripe success webhook redirect the user to the home page with a message 'error retrieving order'

- ##### 404 error page
    ##### Visuals & Responsiveness:
    ##### Functionality:
    ##### Defensive design:

    - The error message is sized and positioned correctly



### User Story Testing

### Automated Testing

### Unresolved Issues

 - On screens below 992px the navbar logo is not centered
 - On screens below 992px, on the farmer map, the zoom buttons are displayed above the main navigation dropdown
 - A product can be added without variants
 - between 992 and 1164 px the main nav links are spaced over two lines
    - fix: add white-space: nowrap to navlinks

 - need to require a variant for products
 - a farmer can purchase their own products if they add them to the cart before logging in

## Planned features:

    - add min_price and max_price fields to products to be able to sort by price

    - product page pagination 
    - 