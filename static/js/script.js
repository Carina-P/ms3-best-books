// jshint esversion:6

/* Global variables */
let search_result = {};
let category_groups = [];

/**
 * On smaller viewports menu should be removed when clicked
 */
$(".js-collapse").on("click", function () { 
  $(".navbar-collapse").collapse("hide");
}); 

/**
 * Move cursor to id search_book_results
 */
function moveTo(){
    window.location.href="#search_book_results";
}

/**
 * When user chooses to not add a book. Reset form and clear part of page
 * that belongs to add a book.   
 */
function cancelAddBook(){
    $("#search_results").html(``);
    $("#add_book").html(``);
    document.getElementById("book_form").reset();
    window.location.href="#book";
}

/**
 * Puts HTML code at #add_book in page. The code fills page with information about book.
 * User is directed to the place in the page with the book information.
 *
 * @param {Object} book contains information about book
 */
function bookToDocument(book){
    if (book === undefined || book === null) {
        console.log(
            "Error in function bookToDocument, book undefined");
            return;
    }

    let text = `<div class="divider-sm"></div>
                <div class="text-center mt-3">
                    <h3>Retrieved information about the Book</h3>
                    <p>Add book further down</p>
                </div>
                <div class="col-12">
                    <div class="card">
                        <div class="card-body bgr-white">
                            <form method="POST" action="/add/book">`;
    
    if ("volumeInfo" in book){
        if ("imageLinks" in book.volumeInfo){
            if ("thumbnail" in book.volumeInfo.imageLinks){
                text += `<div class="text-center">
                            <img src="${book.volumeInfo.imageLinks.thumbnail}" 
                                alt="Picture of book cover">
                        </div>`;
            }
        } 
        if("title" in book.volumeInfo){  
            text += `<div class="col-12 form-group">
                                <label for="title">Title:</label>
                                <textarea id="title" name="title" class="form-control" readonly>${book.volumeInfo.title}</textarea>
                            </div>`;
        }
        
        if("categories" in book.volumeInfo){
            let categories = book.volumeInfo.categories.join(" · ");
            text += `       <div class="col-12 form-group">
                                <label for="category">Category/ies:</label>
                                <textarea id="category" name="category" class="form-control" readonly>${categories}</textarea>
                            </div>`; 
        }
    }

    if ("volumeInfo" in book){
        if ("authors" in book.volumeInfo){
            let authors = book.volumeInfo.authors.join(" · ");
            text += `       <div class="col-12 form-group">
                                <label for="author">Author/s:</label>
                                <textarea id="author" name="author" class="form-control" readonly>${authors}</textarea>
                            </div>`;
        }
        if ("language" in book.volumeInfo){
            text +=        `<div class="col-12 form-group">
                                <label for="language">Language</label>
                                <input id="language" name="language" value="${book.volumeInfo.language}" class="form-control" type="text" readonly>
                            </div>`;
        }
        if ("publishedDate" in book.volumeInfo){
            text +=        `<div class="col-12 form-group">
                                <label for="publish_date">Published Date</label>
                                <input id="publish_date" name="publish_date" value="${book.volumeInfo.publishedDate}" class="form-control type="text" readonly>
                            </div>`;
        }
        if ("industryIdentifiers" in book.volumeInfo){
            let identifier = book.volumeInfo.industryIdentifiers[0].type + ", " + book.volumeInfo.industryIdentifiers[0].identifier;
            text += `       <div class="col-12 form-group">
                                <label for="identifier">Identifier:</label>
                                <input id="identifier" name="identifier" type="text" value="${identifier}" class="form-control" readonly>
                            </div>`;
        }
        if ("description" in book.volumeInfo){
            text += `       <div class="col-12 form-group">
                                <label for="description">Description:</label>
                                <textarea id="description" name="description" class="form-control" readonly
                                    >${book.volumeInfo.description}</textarea>
                            </div>`;
        }
        if ("imageLinks" in book.volumeInfo){
            if ("thumbnail" in book.volumeInfo.imageLinks){
                text += `   <div class="col-12 form-group">
                                <label for="image_link">Image Link:</label>
                                <textarea id="image_link" name="image_link" class="form-control" readonly
                                    >${book.volumeInfo.imageLinks.thumbnail}</textarea>
                            </div>`;
            }
        }
        text += `       <div class="col-12 bgr-acid pt-3 pb-3">
                            <div class="text-center">
                                <h5>Before adding book</h5>
                                <p>Choose category group and, if you want, add an opinion of the book.</p>
                            </div>
                            <div class="input-group mb-3">
                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="category_group">Category Group:</label>
                                </div>  
                                <select id="category_group" name="category_group" class="custom-select" required>
                                    <option value="" disabled selected>Choose...</option>`;
    for (let category_group of category_groups){
        text += `               <option value="${category_group.group_name}">${category_group.group_name}</option>`;
    }
    text += `                   </select>
                            </div>
                            <div class="input-group mb-3">
                                <div class="input-group-prepend">
                                    <label class="input-group-text padding-r17" for="grade">Grade the book:</label>
                                </div>
                                <select id="grade" name="grade" class="custom-select">
                                    <option value="" disabled selected>Choose...</option>`;
    for (let i=5; i>0; i--){
        text += `                   <option value="${i}">${i}</option>`;
    }
    text += `                  </select>
                            </div>
                            <div class="col-12 form-group">
                                <label for="review">Review</label>
                                <textarea id="review" name="review" class="form-control" placeholder="Enter your review"></textarea>
                            </div>
                            <div class="col-12 text-center">
                                <button type="reset" class="btn btn-lg btn-red" onclick="cancelAddBook()">
                                    Cancel <i class="fas fa-times-circle"></i>
                                </button>
                                <button type="submit" class=" btn btn-lg btn-green">
                                    Add Book <i class="fas fa-plus-square"></i>
                                </button>
                            </div>`;
    } else{
        text += `No information about this book.`;
    }

    text += `           </div>
                    </form>
                </div>
            </div>
        </div>`; 

    $("#add_book").html(text);
    window.location.href="#add_book";
}

/**
 * Global variable search_result.items is a list that contains information about books.
 * The function makes information about book at specific index, in list, appear on page.
 *
 * @param {Int} index Place in list search_result.items of book to be shown 
 */
function addBook(index){
     if (index === undefined || index === null) {
        console.log(
            "Error in function addBook, index undefined");
            return;
    }

    let book = search_result.items[index];
    bookToDocument(book);
}

/**
 * Makes HTML code that puts information from global variable search_results into a page.
 * Then the cursor is moved to start of information.
 */
function searchToDocument(){
    let text = `<div class="divider-sm"></div>
                <div class="text-center m-5">
                    <h3>Search results:</h3>
                </div>`;
    
    if (search_result.totalItems==0){
        text += `<div class="text-center mt-3">No books found with the input given.</div>`;
    }
    else{
        let index = 0;
        text += `<div class="row">`;
        for (let book of search_result.items){
            if ("volumeInfo" in book){
                text += `<div class="col-12 col-md-6 col-lg-4 mb-3">
                            <div class="card h-100 text-center">
                                <div class="card-body">`;
                
                if ("title" in book.volumeInfo){
                    text +=`<div class="card-title">
                                <h6>${book.volumeInfo.title}</h6>
                            </div>`;
                }
                if ("imageLinks" in book.volumeInfo){
                    if ("thumbnail" in book.volumeInfo.imageLinks){
                        let image_link = book.volumeInfo.imageLinks.thumbnail;
                        
                        // Make sure the image_link is secure (https)
                        book.volumeInfo.imageLinks.thumbnail = image_link.replace("http:", "https:");
                        text += `<img src=${book.volumeInfo.imageLinks.thumbnail} alt="Picture of book cover">`;
                    }
                }
       
                text += `<div class="card-text">`;
                if ("authors" in book.volumeInfo){
                    for (let author of book.volumeInfo.authors){
                        text += `${author} · `;
                    }
                }
                if ("publishedDate" in book.volumeInfo){
                    text += `<br>${book.volumeInfo.publishedDate}`;
                }

                text += `   </div>
                        </div>
                        <div class="card-footer bgr-white">
                            <button type="submit" class="btn btn-sm btn-green" onclick="addBook(${index})">
                                Choose book <i class="fas fa-hand-pointer"></i>
                            </button>
                        </div>
                    </div>
                </div>`;

                index++;
            }
        }
        text += `</div>`;
    }

    $("#search_results").html(text);
    $("#add_book").html("");
    document.getElementById("book_form").reset();
    window.location.href="#search_results";
}

/**
 * Search for books in Google Books that fits input parameters.
 * Then it calls a function that puts information in page.
 *  
 * @param {String} search_text, the text to match with books in Google Books
 */
function searchForBooks(search_text){
    if (!search_text || search_text.trim().length === 0){
        console.log("No information to search for!");
    }
    else{
        fetch("https://www.googleapis.com/books/v1/volumes?q=" + search_text + "&printType=books&projection=full&maxResults=21&key=AIzaSyAa48h04CAMjJ1bVewMoBx-_8EZv1IBNpI")
        .then(res =>res.json())
        .then(res => {
            // Global variable
            search_result = res;
            searchToDocument();
        })
        .catch(error => {
            console.log("something went wrong when fetching info from Google Books", error);
        });
    }
}

/**
 * When this function is called it starts a search for books in Google Books that have an author with name
 * looking like value retrived from page.
 * 
 * @param {Array} group_names, contains category group names
 */
function searchBooks(group_names){
     if (group_names === undefined || group_names === null) {
        console.log(
            "Error in function searchBooks, group_names undefined");
            return;
        }
    // Put group_names in global parameter
    // Group_names is needed if/when user wants to add book
    category_groups = group_names;

    // Fetch information from page
    let search_books = $("#search_books").val();
    searchForBooks(search_books);
}

/**
 * Put information in a modal and activates the modal.
 * 
 * @param {String} book_id, books id in database 
 * @param {String} title, books title 
 */
function addOpinion(book_id, title){
    if (book_id === undefined || book_id === null) {
        console.log(
        "Error in function addOpinion, book_id undefined");
        return;
    }

    if (title === undefined || title === null) {
        console.log(
        "Error in function addOpinion, title undefined");
        return;
    }

    $("#book_title").html(title);
    $("#hidden_input").html(`<input type="hidden" name="book_id" value="${book_id}">`);
    $('#modal').modal('show');
}

/**
 * Put HTML code for a select, with option 1 to 5, in a string and return it.
 * 
 * @param {String} grade, the option in select that is to be marked "selected" 
 * @return {String}, the resulting code
 */
function selectToDocument(grade){
    if (grade === undefined || grade === null) {
        console.log(
        "Error in function selectToDocument, grade undefined");
        return;
    }
    let text = ``;
    for (let i=5; i>0; i--){
        if (i == Number(grade)){
            text += `<option value="${i}" selected>${i}</option>`;
        }
        else{
            text += `<option value="${i}">${i}</option>`;
        }
    }
    return text;
}

/**
 * Put interesting information into a modal and then activates modal.
 * 
 * @param {String} book_id, books id in database 
 * @param {String} title, title of book 
 * @param {String} review_id, id of current review, in database 
 * @param {Float} grade, grading of book given from user 
 * @param {String} review, review of book given from user 
 * @param {String} return_to, page user should be redirected to when the change is done.
 */
function changeOpinion(book_id, title, review_id, grade, review, return_to){
    if (book_id === undefined || book_id === null) {
        console.log(
        "Error in function changeOpinion, book_id undefined");
        return;
    }
    if (title === undefined || title === null) {
        console.log(
        "Error in function changeOpinion, title undefined");
        return;
    }
    if (review_id === undefined || book_id === null) {
        console.log(
        "Error in function changeOpinion, review_id undefined");
        return;
    }
    if (grade === undefined || grade === null) {
        console.log(
        "Error in function chageOpinion, grade undefined");
        return;
    }
    if (review === undefined || review === null) {
        console.log(
        "Error in function changeOpinion, review undefined");
        return;
    }
    if (return_to === undefined || return_to === null) {
        console.log(
        "Error in function changeOpinion, return_to undefined");
        return;
    }
    $("#book_title").html(title);
    $('#modal_form').attr('action', `/change/opinion/${return_to}/${title}`);
    $("#hidden_input").html(`<input type="hidden" name="book_id" value="${book_id}">
        <input type="hidden" name="review_id" value="${review_id}">`);

    // if there is no grade (grad="0") user can choose a grade as in add opinion
    // else show current grade
    if (grade != "0"){
        $("#grade_m").html(selectToDocument(grade));
    }
    $("#review_m").html(review);
    $('#modal').modal('show');
}