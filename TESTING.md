## Testing

### Code Validation

### Performance

### Responsiveness
This website was designed using a mobile-first approach and was tested for responsiveness on multiple device sizes in addition to browser-simulated devices in Google Chrome Developer Tools and Firefox Developer Tools

Devices Used : Redmi Note 4, Redmi Note 9, Lenovo Tab4 10

Browser device simulation:
    - Google Chrome: Moto G4, Pixel 2 XL, iPhone/SE, iPhone X, iPad, iPad Pro, Galaxy Fold
    - Mozilla Firefox: Microsoft Lumia 950 (Windows Phone 10.0), Galaxy S9/S9+ (Android 7.0), Galaxy Note 3 (Android 4.3)

The following details were verified to ensure the website was responsive and the UI and design were consistent on all devices and browser device simulations:

- #### All pages
    - There is no horizontal overflow from any elements outside the page boundaries

- #### Navbar
    - All links are horizontally and vertically aligned and centered
    - Dropdowns are working correctly and text can be entered into the search box
    - All link text is readable
    - If the cart total is more than 5 digits, there is no overflow and the layout is not affected negatively

- #### Footer
    - The logo, email, phone and about link text is readable
    - On smaller screens, only the icons are displayed for email, phone and about links
    - The logo icon is sized correctly
    - The logo icon attribution is sized correctly

- #### Home

-  Banners
    - The banner image positioning is correct and that the apple basket is visible on all screen sizes
    - The banner text is readable and scales properly across different screen sizes
    - The banner login and register buttons are sized correctly and the text is readable

-  Carousel
    - The carousel slide items are scaled properly across device sizes
    - The carousel doesn't display too many items for the screen width
    - The carousel item text and buttons are readable and properly aligned
    - On mobile devices the carousel items can be swiped
    - The carousel next and previous buttons are sized properly and work as expected

- ##### Login, Registration, Log out, Change Password Pages
    - All text is sized correctly
    - There is adequate spacing around the text, labels, inputs and button
    - The inputs and button are size correctly
    - Any django form validation errors are sized properly and their positioning is correct

- ##### About Page
    - All headings and paragraphs are readable
    - The sections and headings have appropriate padding and positioning

- ##### Farmer Map
    - The heading text is sized and positioned correctly
    - The map zoom and pan works as expected
    - The map markers can be clicked and the marker content is displayed properly

- ##### Product List/Search Results/My Products List
    - The product count heading and sort button text is readable
    - The sort button and dropdown menu are positioned correctly
    - The product card images are sized and positioned correctly
    - The product card text and buttons are sized and positioned correctly
    - If present the search term display is sized and positioned correctly

- ##### Product Detail
    - The product card image is sized and positioned correctly
    - The product card text and add to cart/edit product button is sized and positioned correctly
    - The variant and quantity inputs are sized and positioned correctly

- ##### Product Edit/Create Form, Product delete confirmation
    - The heading, input and label text is sized properly
    - All elements have adequate space and are correctly aligned
    - The dynamic variant subform behaves as expected

- ##### Profile Detail
    - The profile card image is sized and positioned correctly
    - The profile card text and edit profile button is sized and positioned correctly
    - The product card images, text and 'details' button are all sized and positioned correctly

- ##### Profile Edit/Create Form, Checkout Form, Profile delete confirmation
    - The heading, input and label text is sized properly
    - All elements have adequate space and are correctly aligned
    - The button text and loading icon are displayed correctly when fetching the geocoding data on the address forms

- ##### Cart
    - The headings, cart items and button text are all readable
    - The product items are spaced evenly and the buttons work as expected

- ##### Payment form/ Checkout complete
    - All headings and text are sized and positioned correctly
    - All order items are sized and positioned correctly
    - The delivery information notice is positioned correctly
    - The customer details are displayed correctly
    - The card form, card validation errors, and card loading spinner are displayed correctly

- ##### Order list
    - All headings and order titles are readable
    - There is adequate spacing around all elements

- ##### Order detail, Farmer order detail
    - All headings and text are sized and positioned correctly
    - All order items are sized and positioned correctly
    - The delivery information notice is positioned correctly
    - The customer details are displayed correctly

- ##### 404 error page
    - The error message is sized and positioned correctly



### Defensive Design Testing

### User Story Testing

### Automated Testing

### Unresolved Issues

 - On screens below 992px the navbar logo is not centered
 - On screens below 992px, on the farmer map, the zoom buttons are displayed above the main navigation dropdown
 - A product can be added without variants
 - between 992 and 1164 px the main nav links are spaced over two lines
    - fix: add white-space: nowrap to navlinks
