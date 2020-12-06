let search_result = {};
let category_groups = [];

$(document).ready(function(){
    $('.sidenav').sidenav({edge:"right"});
    $('select').formSelect();
});

function cancelAddBook(){
    $("#add_book").html(``);
    window.location.href="#search_results";
}

function bookToDocument(book){
    console.log(book);

    let text = `<div class="center-align">
                    <h3>Book to Add</h3>
                </div>
                <div class="center-align">
                    <p>Choose category group(mandatory) and give your opinion(voluntary) of the book, before you add it.<br>
                    Book information below (if you can not see whole text: resizing is possible by pointing and moving the bottom right corner).</p>
                </div>
                <div class="col s12 m10 offset-m1">
                    <div class="card">
                        <div class="card-content bgr-white">
                            <form>`;
    
    if ("volumeInfo" in book){
         if("title" in book.volumeInfo){  
            text += `<div class="col s12">
                                <label for="title">Title:</label>
                                <input id="title" name="title" type="text" value="${book.volumeInfo.title}" readonly>
                            </div>`;
        }
        if ("imageLinks" in book.volumeInfo){
            if ("thumbnail" in book.volumeInfo.imageLinks){
                text += `<div class="center-align">
                            <img src="${book.volumeInfo.imageLinks.thumbnail}" 
                                alt="Picture of book cover">
                        </div>`;
            }
        }
        if("categories" in book.volumeInfo){
            let categories = book.volumeInfo.categories.join(" · ");
            text += `       <div class="col s12">
                                <label for="category">Category/ies:</label>
                                <input id="category" name="category" type="text" value="${categories}" readonly>
                            </div>`; 
        }
    }

    text += `           <div class="col s12">
                            <label for="category_group"></label>
                            <select id="category_group" name="category_group" class="validate" required>
                                <option value="" disabled selected>Choose Category Group</option>`;
    for (category_group of category_groups){
        text += `              <option value="${category_group}">${category_group}</option>`;
    }
    text += `               </select>
                        </div>
                        <div class="col s12">
                            <label for="grade"></label>
                            <select id="grade" name="grade" class="validate">
                                <option value="" disabled selected>Grade book</option>
                                <option value="5">5</option>
                                <option value="4">4</option>
                                <option value="3">3</option>
                                <option value="2">2</option>
                                <option value="1">1</option>
                            </select>
                        </div>
                        <div class="col s12">
                                <label for="review">Your review of the book</label>
                                <textarea id="review" name="review"></textarea>
                        </div>
                        <div class="row">
                            <div class="col s12 center-align">
                                <button type="reset" class="btn-large btn-red waves-effect waves-light" onclick="cancelAddBook()">
                                    Cancel <i class="fas fa-times-circle right"></i>
                                </button>
                                <button type="submit" class="btn-large btn-green waves-effect waves-light">
                                    Add <i class="fas fa-plus-square right"></i>
                                </button>
                            </div>
                        </div>
                        <div class="center-align section">
                            <h5>Book Information:</h5>
                        </div>
                        <div class="row">`;

    if ("volumeInfo" in book){
        if ("authors" in book.volumeInfo){
            let authors = book.volumeInfo.authors.join(" · ");
            text += `       <div class="col s12">
                                <label for="author">Author/s:</label>
                                <textarea id="author" name="author" class="materialize-textarea" maxlength="200" readonly
                                    >${authors}</textarea>
                            </div>`;
        }
        if ("language" in book.volumeInfo){
            text +=        `<div class="col s12">
                                <label for="language">Language</label>
                                <input id="language" name="language" value="${book.volumeInfo.language}" type="text" readonly>
                            </div>`;
        }
        if ("publishedDate" in book.volumeInfo){
            text +=        `<div class="col s12">
                                <label for="publish_date">Published Date</label>
                                <input id="publish_date" name="publish_date" value="${book.volumeInfo.publishedDate}" type="text" readonly>
                            </div>`;
        }
        if ("industryIdentifiers" in book.volumeInfo){
            let identifier = book.volumeInfo.industryIdentifiers[0].type + ", " + book.volumeInfo.industryIdentifiers[0].identifier;
            text += `       <div class="col s12">
                                <label for="identifier">Identifier:</label>
                                <input id="identifier" name="identifier" type="text" value="${identifier}" readonly>
                            </div>`;
        }
        if ("description" in book.volumeInfo){
            text += `       <div class="col s12">
                                <label for="description">Description:</label>
                                <textarea id="description" name="description" class="materialize-textarea" readonly
                                    >${book.volumeInfo.description}</textarea>
                            </div>`;
        }
        if ("imageLinks" in book.volumeInfo){
            if ("thumbnail" in book.volumeInfo.imageLinks){
                text += `   <div class="col s12">
                                <label for="image_link">Image Link:</label>
                                <textarea id="image_link" name="image_link" class="materialize-textarea" readonly
                                    >${book.volumeInfo.imageLinks.thumbnail}</textarea>
                            </div>`;
            }
        }
    } else{
        text += `No information about this book.`;
    }

    text += `           </div>
                    </form>
                </div>
            </div>
        </div>`; 

    $("#add_book").html(text);
    $('select').formSelect();
    window.location.href="#add_book";
}

function addBook(index){
    console.log(index, typeof(index));
    let book = search_result.items[index];
    console.log(book);
    bookToDocument(book);
}

function searchToDocument(){
    let text = `<div class="center-align">
                <h3>Search results:</h3>
            </div>`;
    
    if (search_result.totalItems==0){
        text += `<div>No books found with the input given.</div>`;
    }
    else{
        let index = 0;
        for (book of search_result.items){
            if ("volumeInfo" in book){
                text += `<div class="col s12 m6 l4">
                            <div class="card medium center-align">`;
                
                if ("imageLinks" in book.volumeInfo){
                    if ("thumbnail" in book.volumeInfo.imageLinks){
                        text += `   <div class="card-image">
                                        <img src=${book.volumeInfo.imageLinks.thumbnail}>
                                    </div>`;
                    }
                }
                text += `   <div class="card-content">`;
                if ("title" in book.volumeInfo){
                    text +=`        <h6>${book.volumeInfo.title}</h6>`;
                }
                text += `<p>`;
                if ("authors" in book.volumeInfo){
                    for (author of book.volumeInfo.authors){
                        text += `${author} · `;
                    }
                }
                if ("publishedDate" in book.volumeInfo){
                    text += `${book.volumeInfo.publishedDate}`;
                }

                text += `   </p>
                        </div>
                        <div class="card-action">
                            <button type="submit" class="btn-small btn-green waves-effect waves-light" onclick="addBook(${index})">
                                Add this book
                            </button>
                        </div>
                    </div>
                </div>`;

                index++;
            }
        }
    }
    $("#search_results").html(text);
    window.location.href="#search_results";
}

function searchForBooks(title_or_author, search_text){
    if (!search_text || search_text.trim().length === 0){
        console.log("ingen info");
    }
    else{
        console.log(search_text);
        console.log(title_or_author);
        fetch("https://www.googleapis.com/books/v1/volumes?q="+ title_or_author + ":" + search_text + "&printType=books&projection=full&key=AIzaSyAa48h04CAMjJ1bVewMoBx-_8EZv1IBNpI")
        .then(res =>res.json())
        .then(res => {
            console.log(res);
            search_result = res;
            searchToDocument();
        })
        .catch(error => {
            console.log("something is wrong", error);
        });
    }
}

function searchTitle(group_names){
    console.log("Sök title");
    category_groups = group_names;
    console.log(category_groups);
    let search_title = $("#search_title").val();
    searchForBooks("intitle", search_title);
}

function searchAuthor(group_names){
    console.log("Sök författare");
    category_groups = group_names;
    let search_author = $("#search_author").val();
    searchForBooks("inauthor", search_author);
}