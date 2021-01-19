# ![](https://github.com/Carina-P/ms3-best-books/blob/master/static/favicon/favicon.ico?raw=true)      Best Books

This is the site where you get inspired and find new books to read. 
You will find descriptions of different books and also reviews with other
readers best tips.
You are also welcome to add your own reviews and tips.

The live project can be found here: [https://ms3-best-books.herokuapp.com/](https://ms3-best-books.herokuapp.com/)

## UX
### Strategy Plane
#### Site owner's goal
- Earn money on each book purchased via link from the site.
- Get inspired from users reviews and recommendations.


#### External users goal
Find books they would like to read.

There are three types of users:
- Those who just want to get inspiration and find books to read: **Viewer**.
- Those who also want to add books to the site and share their thoughts
 about a book/books: **Reviewer**.
- The administrator of the page who manages book categories: **Administrator**.

**Site owners need**
- That it is easy for user to buy book: priority 1.

**Viewers and Reviewers** needs:
- Easy and intuitive way to browse books: priority 1.
- Easy find more information about a book: priority 2.
- Buy book/s. 
- See what other users think about book: priority 2.

**Reviewers** needs:
- Easy search for a book and add book that is not present on site: priority 2.
- Easy grade and give review of book: priority 2.
- Update and remove "own books" (books that user has added) :  priority 3.
- Update and remove "own reviews" (reviews that user has added): priority 3.

**Administrators** needs:
- Authority to edit and remove all ideas of all users: priority 3.
- Authority to manage categories: priority 3.

### Scoope Plane
#### User stories
- US_001: As a user I want to browse for a book.
- US_002: As a user I want to see detailed information about a book. 
- US_003: As a user I want to buy a book
- US_004: As a user I want to see which books are most popular on the site.
- US_005: As a user I want to look for most popular books in a category.
- US_006: As a user I want to add book to the site.
- US_007: As a user I want to edit information about the book.
- US_007: As a user I want to remove book.
- US_008: As a user I want to grade a book.
- US_009: As a user I want to review a book.
- US_010: As a user I want to edit my opinion of a book.
- US_011: As a user I want to remove my opinion of a book.
- US_0012: As a user I want to register (sign up) to the system.
- US_0013: As a user I want to log in to the system.
- US_0014: As a user I want to log out of the system.
- US_0015: As a "administration" user I want to add categories.
- US_0016: As a "administration" user I want to edit and remove categories.

#### Features
- Search for books. 
- Search for books belonging to category.
- Easy to buy a book with a link.
- Overview: many books with limited information for each book.
- Possibility to easily get more detailed information about a book.
- Add, edit and remove a book.
- When adding a book: "help" to "automatically" fill in information about the book.
- Add, edit and remove review and grade for a book.
- Authentications system: User can only edit and remove "own books" and 
"own reviews".
- Add, edit and remove categories. Authentication system limits this
capability to those with administator privleges.

### Structure Plane
- The site starts with the homepage: "Books", where you can search and find books.
- From navbar you can choose to Register, Log In/Log Out and Manage Categories, 
depending on your authorities.
- From "Books" you reach:
    - "Book Details/ Manage Book" with more details about book. Here user also can add
opinion about book and manage user own opinions. User can edit and remove if it is 
users "own" book. If user deletes book: all opinions is also deleted. When book is 
removed, user is redirected to homepage.
    - "Add Book": User search with title or author and gets suggestions from system
that user choose between. After adding a book user is moved to 
"Book details/Manage Book" page.
    - Result from book search. User can choose a book from search-result and 
being redirected to "Book details/Manage Book".

- "Register", "Log In" and "Manage Categories" has separate pages.

Here is a visual of the structure:
![](https://github.com/Carina-P/ms3-best-books/blob/master/wireframes/structure.jpg?raw=true)

### Skeleton Plane
- The user browses via navigation system.
- User searches for book/s by giving book title or author or part of it.
- User can filter search by giving categories
- Interactive design that works on Mobile, Tablet as well as Desktop.
#### Wireframes
- [Mobile](https://github.com/Carina-P/ms3-best-books/blob/master/wireframes/wireframe-mobile.pdf)
- [Tablet](https://github.com/Carina-P/ms3-best-books/blob/master/wireframes/wireframe-tablet.pdf)
- [Desktop](https://github.com/Carina-P/ms3-best-books/blob/master/wireframes/wireframe-desktop.pdf)

##### Major changes compared to wireframes

#### Data structure
According to project instructions the document-based 
database MongoDB is used. Here is a visual of the collections:
![](https://github.com/Carina-P/ms3-best-books/blob/master/database/database-design.jpg?raw=true)

- Both books and books_details contain information about books. I decided to 
divid the information into two collections using the **subset pattern**
([Mongo DB Documentation](https://docs.mongodb.com/manual/tutorial/model-embedded-one-to-one-relationships-between-documents/))
The information in books collection is accessed often from the page but information in the books_details
collection is less frequently-accessed.
- The **subset pattern** 
([MongoDB Documentation](https://docs.mongodb.com/manual/tutorial/model-embedded-one-to-many-relationships-between-documents/)) 
is also used for book_details and reviews collections.
It is possible to add a huge amount of reviews and I deceided to embed the five 
latest reviews in the books_details collection.
This five (or fewer if less reviews) reviews will be shown together with the 
book details. User is given possibility to see more reviews and then all
reviews are fetched from review collection.

#### Design Choices
##### Fonts
For this project the Google Font Poppins is choosen. Poppins is a newcommer in
the geometric sans serif typefaces tradition. It is a rounded and modern fontawesome
that I think feels friendly and fits on this site.
As alternative Google Font Roboto is choosen.

##### Colours
**Text and background**
![](https://github.com/Carina-P/ms3-best-books/blob/master/wireframes/text-colour.png)
- Floral White, #fffcf2, is used for background most of the time. But also for
text on dark background.
- Black Coffe, #32292f, is used for text most of the time. But also for text on
light background.

Floral White and Black Coffe is chosed because they are a little softer than 
White, #ffffff, and Black, #000000, respectively. But they still give good
contrast when used together.

**For attention**
![](https://github.com/Carina-P/ms3-best-books/blob/master/wireframes/category-colour.png)
The following colours are used for the different categories. One or some of 
them will also be used to draw attention to e.g. buttons. For me this is autumn
colours and autumn is a good season to read a book.
- Charcoal, #264653
- Persian Green, #2a9d8f
- Sandy Brown, #f4a261
- Burnt Sienna, #e76f51
- Madder Lake, #cc2936
- Coffee, #774936
<!--
Use this section to provide insight into your UX process, focusing on who this website is for, what it is that they want to achieve and how your project is the best way to help them achieve these things.

In particular, as part of this section we recommend that you provide a list of User Stories, with the following general structure:
- As a user type, I want to perform an action, so that I can achieve a goal.

This section is also where you would share links to any wireframes, mockups, diagrams etc. that you created as part of the design process. These files should themselves either be included as a pdf file in the project itself (in an separate directory), or just hosted elsewhere online and can be in any format that is viewable inside the browser.
-->
## Features
<!--
In this section, you should go over the different parts of your project, and describe each in a sentence or so.
-->
### Existing Features
- Features in all pages:
    - **Messages** to the user is shown in top of current page, with an "acid green" background colour.
    - **Header**:
    - logo and navbar fixed at the top of viewport:
        - **logo**: When hover over, it becomes larger
        - **navbar**: When hover over links, the color changes
        - If **medium and smaller**  viewport widths: links are collapsed to a "hamburger" menu.
    - **Footer**: In bottom of page with **social links**.

- **Home page** and other pages reached from the home page:
    - **Start**, Welcome on a background image:
        - Short introduction to the site
    - **Top ten** most popular books in a **carousel**:
        - Possibility to **buy the book**: In top right corner is a read shopping cage with a link. 
        Hoovering the link makes picture larger.        
        - Possibility to link to more **details of the book**
        - If user i logged in also possibility to **add opinion** about the book.
    - **Best in category**:
        - All **category groups** present in database is shown with **different background colours**.
        - Possibility to **click on a category group** and then user is moved to **result-page** that shows
        **most popular books within choosen category group**.
        - If **no book** in database is attached to the category group - a **message** is shown in top of page.
    - **Search for book in database**:
        - A **search-form** where user can print title/part of title, author or part of authors name and then search
        for books. Result is shown in **result-page**. The link to submit the search is called "Search Book" and this 
        is according to Google Books [Branding Guidlines](https://developers.google.com/books/branding): 
        "You may only use the verbs "Search," "Search Books," or "Search in this book" 
        when prompting users for action that results in an API query (e.g., on a form 'submit' button)." 
        - If **no book** in database **matches** the search - a **message** is shown in top of page.
    - **Add book** - this feature is only available to users that are logged in:
        - User do not have to know all information about a book. Instead user **searches in the API: Google Books**
        for the book with information to add to the database.
        - A **search-form** where user can print title/part of title and or author/part of authors name.
        - The **resulting books** matching the search-criteria is **shown below** the search-form when user clicks search or 
        presses return. User is moved to the place.
        - The user continues with choosing which book he/she is interested in adding. When book is choosen, 
        **more details about the book** is shown, in a **form**, further down. And user is moved to this place.
        - **Finally** the user chooses a **category group** that book should be attached to in this database. User can also, voluntarily,
        **add a grade and a review** of the book before submitting to the database.
        - If user does not want to add book - he/she can click on **Cancel** and the information is removed and user
        redirected to the search-form for adding book.

- **Search-result page**:
    - User ends up at this page when either:
        - looking for **most popular** books belonging to a **category group** or
        - **searching** for a book **in this database**
    - **"Card deck"** of books i shown with:
        - Possibility to **buy** each book.
        - **Title, image of cover, author/s** and 
        - Information which **average grade** book is given in this database.
        - Possibility to go to **"book-details page"** with more information about choosen book.
        - If user has logged in - there is also a possibility to **add opinion** of the book.
    - **Close-Button** in top right corner takes user back to home-page.

- **Book-details page**:
    - User ends up at this page when choosing **"Book Details"-button** either in top-ten **carousel** or
    in **book-card** in search-result page.
    - The following information of the book is shown:
        - **Title**
        - **Image of book cover**
        - **Author/s**
        - **Published date**
        - **Average grade** in this database. Grade is also represented by  **filled stars**.
        - **Category in Google Books**
        - **Category group** choosen for the book by user who added the book.
        - **Identifier**
        - **Description**
        - Username of **user who added the book**.
    - Up to **five** of the **latest opinions** given to the book is shown, with information:
        - Of **who** gave the opinion
        - **Grade** given
        - And the **review** given
    - If **more than five opinions** is give to the book:
        User is given opportunity to go to **reviews-page** with all opinions given to the book.
    - User who has added the book can also **delete** it. When book is deleted all opinions about the book are also deleted.
    - It is possible to **add an opinion**:
        - When this alternative is choosen an **add opion modal** is shown..
    - User who has added an opinion can also **edit or delete the opinion**.
    - If **Edit opinion** is choosen an **edit opinion modal** is shown.
    - **Close-Button** in top right corner takes user back to home-page.

- **Reviews page**:
    - User ends up at this page when **"See all reviews"** is choosen in "Book details page".
    - All opinions of current books is shown, with information about:
        - **Who** has given the opinion
        - **Grade** given
        - **Review** given.
    - **User who has added the opinion** has the possibilities to:
        - **Change** review
        - **Delete** review

- **Add opinion modal**:
    - Modal contains:
        -  Book **title**
        - **select-list** (1 to 5) for **grading** the book
        - text-area for the **review** to be given in
    - When information is submitted:
        - if a grade is given a new average grade is calculated for the book and average grade for book in 
        database is updated.
        - Opinion is added to the database.
        - user is directed to page, which is updated the added opinion, modal was called from.
    - If modal is closed without submitting, user is returned to page where it was called from and no
    updating of database takes place.

- **Edit opinion modal**:
    - Modal contains:
        -  Current books **title**
        - **select-list** with **grade** given to the book
        - text-area with given **review**
        - Grade and/or review can be changed.
    - When information is submitted:
        - If grade is changed a new average grade for book is calculated and updated in the database.
        - Grade and/or review is updated in database.
        - user is directed to page, which is updated with changed grade and/or review, modal was called from.
    - If modal is closed without submitting, user is returned to page where it was called from, and no updating of database occurs.

- **Authorisation pages**:
    - **Log In** and **Sign in** are similar including:
        - **Form** where user can give:
            - **Username** and
            - **Password**
        - **Submitting**:
            - **Password** sent over internet and stored in database, is **hashed**.
            - **Sign In, username is checked** if it already exists. If it does, user is informed and
            **returned to sign In page**. If username does not exist - user is **logged in and redirected to home page**.
            - **Log in, username and password is checked**. If they does not exists or password is 
            wrong: user is informed and **returned to login page**. If correct user is **redirected to 
            home page**.
        - Possibility to go to Sign up and Log in page respectively.

- **Manage Categories pages**:
    - Notice: The category group **Other** can not be changed or deleted.
    - At the moment, anyone who has logged in, can reach this pages. In the future **only users, with
    authority** is allowed to use these pages. And the users, with given authority, are supposed be more experienced 
    of this site and know what to do. **First time users** might be **confused** by what "Managing category groups"
    means.
    - **Category groups page**:
        - A page with all category groups represented in a **"card deck**.
        - User can **add a category group** by clicking on link. User is then redirected to "Add category group page"
        - For each category group user can:
            - **Edit** category group, by clicking on link and is then redirected to "Edit category group page" 
            - **Delete** category group. If category group is deleted. All **books** in database that are **attached to 
            deleted category group** is updated with the category group: **Other**.
    - **Add category group page**:
        - A **form** where user types new category groups name.
        - When form is submitted, new category group is added to the database and user redirected to "Category groups page".
        "Category groups page" is updated with the new category group.
        - If user clicks on cancel, he/she is returned to "Category groups page".
    -**Edit category group page**:
        - A **form** where current category groups name is given.
        - User can edit the name and click on the **Submit-button**. When changed name is submitted:
        Database for all **books attached to category groups name is updated** to the changed category groups name.

### Features Left to Implement
- Whenever user **deletes** a book or an opinion a question of **"are you sure"** should be answered before deletion takes place.
- Implementing **authorisation for managing category groups**. Only a few selected user should be able to do this.
- Ability to **change category group** attached to a book. No other book information can be changed, since the information is
fetched from Google Books API. That is how I interpret the Google Books [branding policy](https://developers.google.com/books/branding).
- It is easy to replace modal with an **affiliate link** when clicking on buy a book.
- Add **indexes** to the database to speed up searching.
- Put **image of book cover in add opinion-modal**, especially when choosing add opinon from book in carousel in home page. since
carousel continues "moving" behind the modal, perhaps user gets confused which book opinion is added to. Notice: Books titel is
given in modal and that is why this feature is not prioritized.

## Technologies Used
<!--
In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.
-->
- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
### Languages
- HTML
    - to structure the web content
    - [https://developer.mozilla.org/en-US/docs/Web/HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- CSS
    - to describe the web page's appearance/presentation
    - [https://www.w3.org/Style/CSS/](https://www.w3.org/Style/CSS/)
- JavaScript
    - to provide interactivity and logic
    - [https://www.javascript.com/](https://www.javascript.com/)
- Python
    - to manage information on server side
    - [https://www.python.org](https://www.python.org)
- Jinja
    - for templating logic
    - [https://jinja.palletsprojects.com/en/2.11.x/](https://jinja.palletsprojects.com/en/2.11.x/)


### Libraries
- Flask
    - a micro framework that makes it easy to manage databases from python
    - [https://flask.palletsprojects.com/en/1.1.x/](https://flask.palletsprojects.com/en/1.1.x/)
- Werkzeug
    - used in this app for authentication
    - [https://werkzeug.palletsprojects.com/en/1.0.x/](https://werkzeug.palletsprojects.com/en/1.0.x/)
- PyMongo
    - enables interaction with the MongoDB database through Python 
    - [https://flask-pymongo.readthedocs.io/en/latest/](https://flask-pymongo.readthedocs.io/en/latest/)
- JQuery
    - to simplify DOM manipulation.
    - [https://jquery.com/](https://jquery.com/)
    
!!!!- [JSON](https://www.json.org/json-en.html)
    - A data-interchange format used when retrieve information from other 
    sources as [Weather Unlocked](http://www.weatherunlocked.com/)
- Font Awesome
    - to use icons
    - [https://fontawesome.com](https://fontawesome.com)
- Materialize
    - to add styling and interactivity
    - [https://materializecss.com](https://materializecss.com)

### Other tools
- MongoDB
    - the database used in this project
    - [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
!!!!- Color blind filter
    - to check the used color palette
    - [https://www.toptal.com/designers/colorfilter](https://www.toptal.com/designers/colorfilter)
!!!!- GT Metrix
    - to check the loading times
    - [https://gtmetrix.com](https://gtmetrix.com)
- Google Fonts
    - got the fonts used
    - [https://fonts.google.com/](https://fonts.google.com/)
- JSHint
    - to check JavaScript
    - [https://jshint.com](https://jshint.com)
- Markup Validation Service
    - to check HTML
    - [https://validator.w3.org](https://validator.w3.org)
- CSS Validation Service
    - to check CSS
    - [https://jigsaw.w3.org/css-validator/](https://jigsaw.w3.org/css-validator/)
!!!!- Autoprefixer CSS online
    - to add vendor prefixes
    - [https://autoprefixer.github.io](https://autoprefixer.github.io)
- GitPod
    - used for version control by utilizing the GitPod terminal to
    commit to Git and push to GitHub and Heroku.
    - [https://gitpod.io/](https://gitpod.io/)
- Heroku
    - to host the web app
    - [https://www.heroku.com](https://www.heroku.com/home)
- Balsamiq
    - for designing the wireframes
    - [https://balsamiq.com/](https://balsamiq.com/)
- Coolors
    - to generate color-schemes
    - [https://coolors.co/](https://coolors.co/)
- Favicon
    - to generate Favicon
    - [https://favicon.io/](https://favicon.io/)
- [ImageOptim](https://imageoptim.com/api)
    - To optimize images to load faster.    

## Testing
"All tests passed without major issues?"
The tests conducted are detailed in [TESTS.md](https://github.com/Carina-P/ms3-best-books/blob/master/TESTS.md)
 <!---
 In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.
 
Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.)
-->
## Deployment
<!--
This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.
-->

## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from [pixabay](https://pixabay.com/)
    - Picture in start page, a book and a cup of coffee, photographer: [Daria-Yakovleva](https://pixabay.com/sv/users/daria-yakovleva-3938704/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2151200)
    - Picture in above navbar on some pages, part of bookshelf, photographer: [Lubos Houska](https://pixabay.com/sv/users/luboshouska-198496/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1204029")
    - Picture in authorisation page, of a woman reading by the sea, photographer: [StockSnap](https://pixabay.com/sv/users/stocksnap-894430/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=925589)
### Acknowledgements

- I received inspiration for this project from X