let books = [];
let category_groups = [];

$(document).ready(function(){
    $('.sidenav').sidenav({edge:"right"});
    $('select').formSelect();
});


function bookToDocument(book){
    console.log(book);

    let text = `<div class="center-align">
                    <p>Choose category group for the book before it is added to the site. Book information below.</p>
                </div>
                <div class="col s12 m10 offset-m1">
                    <div class="card">
                        <div class="card-content bgr-white">
                            <form>`;
    
    if ("volumeInfo" in book){
        if ("imageLinks" in book.volumeInfo){
            if ("thumbnail" in book.volumeInfo.imageLinks){
                text += `<div class="center-align">
                            <img src="${book.volumeInfo.imageLinks.thumbnail}" 
                                alt="Picture of book cover">
                        </div>`;
            }
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
                        <div class="row">
                            <div class="col s12 center-align">
                                <a href="{{url_for('get_books')}}" class="btn-large btn-red waves-effect waves-light">
                                    Cancel <i class="fas fa-times-circle right"></i>
                                </a>
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
        if("title" in book.volumeInfo){       
            text += `   <div class="input-field col s12">
                            <label for="title">Title:</label>
                            <input id="title" name="title" type="text" value="${book.volumeInfo.title}" readonly>
                        </div>`;
        }
        if("categories" in book.volumeInfo){
            let categories = book.volumeInfo.categories.join(" · ");
            text += `       <div class="col s12">
                                <label for="category">Category/ies:</label>
                                <input id="category" name="category" type="text" value="${categories} readonly>
                            </div>`; 
        }
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
                                    >http://books.google.com/books/content?id=DKcWE3WXoj8C&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api</textarea>
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

    $("#search_results").html(``);
    $("#add_book").html(text);
    $('select').formSelect();
    window.location.href="#book";
}

function addBook(index){
    console.log(index, typeof(index));
    let book = books[index];
    console.log(book);
    bookToDocument(book);
}

function searchToDocument(result){
    let text = `<div class="center-align">
                <h3>Search results:</h3>
            </div>`;
    
    if (result.totalItems==0){
        text += `<div>No books found with the input given.</div>`;
    }
    else{
        let index = 0;
        for (book of result.items){
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
                    publish_year = book.volumeInfo.publishedDate.substr(0,4);
                    text += publish_year;
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
            books = res.items;
            console.log(books);
            searchToDocument(res);
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

function searchAuthor(category_groups){
    console.log("Sök författare");
    let search_author = $("#search_author").val();
    searchForBooks("inauthor", search_author);
}