# Test plan

Back to [README](https://github.com/Carina-P/ms3-best-books/blob/master/README.md)

The bellow plan for testing was followed during development of the site:
The TDD, **TestDriven Development**, process is followed. Test cases is
developed/thought off, before code is implemented. The test process is
conducted in an iterativ manner and implementation cycles are short with
small code parts every time. 

Before new code is commited, testing of all code developed earlier are
tested again.

When all features are implemented and tested the following tests are 
performed:
- Go through the test cases for functional testing and testing of
responsiveness, as described below
- **HTML-code validated** by 
[W3S Markup validation service](https://validator.w3.org/)
- **CSS-cod validated** by 
[W3S CSS validation service](https://jigsaw.w3.org/css-validator/)
- **JavaScript-code validated** by [JSHint](https://jshint.com/)
- The site is tested on different browsers, as described below
- The deployed version is tested

<!-- Manual testing only or automated tests also? - description of each!! -->

## Tests of functionality and responsiveness
Functionality tests and tests of responsiveness is done by following test cases
below.
Test of responsiveness is mainly performed with help of Chrome Developers Tool. 
But the site is also tested with iPad mini and iPhone8.

### Test cases

Testing use case US_001: As a user I want to browse for a book.
**TC_001** Browse for a book by giving the books title:
- How to test:
    - Go to form for searching.
    - Print "Where the crawdads sings" in the form
    - Press return
- Expected outcome:
    - View is moved to the page's "Search results" part.
    - The book is found there. Or message that book is not present in site.
**TC_002** Browse for book by giving an author:
- How to test:
    - Go to form for searching.
    - Print "August Strindberg" in the form
    - Press return
- Expected outcome:
    - View is moved to the page's "Search results" part.
    - Book written by August Strindberg is found there. Or message that book is
    not present in site.
**TC_003** Browse for book by giving part of title
- How to test:
    - Go to form for searching.
    - Print "crawdads sings" in the form
    - Press return
- Expected outcome:
    - View is moved to the page's "Search results" part.
    - The book is found there. Or message that book/s is not present in site.
**TC_004** Browse for book by giving part of an authors name:
- How to test:
    - Go to form for searching.
    - Print "August" in the form
    - Press return
- Expected outcome:
    - View is moved to the page's "Search results" part.
    - Book/S written by August Strindberg is found there. Or message that book is
    not present in site.

Testing use case US_002: As a user I want to see detailed information about a book. 
**TC_005** See detailed information about a book
- How to test:
    - Go to list of most popular books
    - Choose one of the books and press details link/button.
- Expected outcome:
    - Page "About book" appears with information about choosen book.

Testing use case US_003: As a user I want to buy a book
**TC_006** Buy a book
- How to test:
    - Go to list of most popular books
    - Choose one book and press buy-link/button
- Expected outcome:
    - Linked to a page with possibility to buy the choosen book

Testing use case US_004: As a user I want to see which books are most popular on the site.
**TC_007** See the most popular books on the site
- How to test:
    - Go to homepage and look for the header: "Most popular books" or
    - Use navigation bar and choose "Popular"
- Expected outcome:
    - Moved to view that shows a list with the sites most popular books,
    including average grade for each book.

Testing use case US_005: As a user I want to look for book in a category.
**TC_008** Look for a book in a category
- How to test:
    - Go to navigation bar and choose "Categories"
    - Press button/link that says "Mystery and Thriller"
- Expected outcome:
    - Moved to view that shows search results
    - Books within the category should be shown in the results.

Testing use case US_006: As a user I want to add book to the site.
**TC_009** Add book
- How to test:
    - Log in, if needed sign in first
    - In navigation bar choose: "Add Book"
    - In "search-form" print: "Pippi Longstocking"
    - Press "Add book to this site" for the book from 2020 in the search-results
- Expected outcome:
    - Moved to page "Book details/Manage Book" with information about
    the book that now has been added.
    - Also when on homepage searching for "Pippi Longstocking" the book added
    should appear in search list

Testing use case US_007: As a user I want to edit information about a book.
**TC_010** Edit book information
- How to test:
    - Log in with same user as added Pippi Longstocking
    - Search in search-form for "Pippi Longstocking"
    - In search result, find "Pippi Longstocking"
    - Press "Book Details"-button/link
    - In "Book details/Manage Book"-page press "Edit book info"
    - Change author to "A Lindgren"
    - Press "Submit/Save"-button
- Expected outcome:
    - When looking at the book the author is A Lindgren instead of Astrid 
    Lindgren.

Testing use case US_008: As a user I want to remove book.
**TC_011** Remove book
- How to test:
    - Log in with same user as added Pippi Longstocking
    - Search in search-form for "Pippi Longstocking"
    - In search result, find "Pippi Longstocking"
    - Press "Book Details"-button/link
    - In "Book details/Manage Book"-page press "Edit book info"
    - Change author to "A Lindgren"
    - Press "Submit/Save"-button
- Expected outcome:
    - When searching for the book it no longer appears on the site.

- US_009: As a user I want to grade a book.
- US_010: As a user I want to review a book.
- US_011: As a user I want to edit my opinion of a book.
- US_012: As a user I want to remove my opinion of a book.
- US_0013: As a user I want to register to the system.
- US_0014: As a user I want to log in to the system.
- US_0015: As a user I want to log out of the system.
- US_0016: As a "administration" user I want to add categories.
- US_0017: As a "administration" user I want to edit and remove categories.

#### Test protocol
## UX testing
UX testing is conducted by watching and interviewing users when they used
the page. Examples of issues/discussions:

## Code validation
## Different browsers

## Some of the bugs

## Remaining bugs