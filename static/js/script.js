let search_result = {};
let category_groups = [];

$(document).ready(function(){    
/*
    $('#next').click( () => {
        $('.carousel.carousel-slider').carousel('next');
    });
    $('#prev').click( () => {
        $('.carousel.carousel-slider').carousel('prev');
    });
*/
});

function cancelAddBook(){
    $("#add_book").html(``);
    window.location.href="#book";
}

function moveTo(){
    window.location.href="#search_category";
}

function bookToDocument(book){
    let text = `<div class="text-center mt-3">
                    <h3>Retrieved information about the Book</h3>
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
    text += `           <div class="bgr-acid p-3">
                            <div class="text-center">
                                <h5>Before adding book</h5>
                                <p>Choose category group(mandatory) and give your opinion(voluntary) of the book.</p>
                            </div>
                            <div class="input-group mb-3">
                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="category_group">Category Group:</label>
                                </div>  
                                <select id="category_group" name="category_group" class="custom-select" required>
                                    <option value="" disabled selected>Choose...</option>`;
    for (category_group of category_groups){
        text += `               <option value="${category_group.group_name}">${category_group.group_name}</option>`;
    }
    text += `                   </select>
                            </div>
                            <div class="input-group mb-3">
                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="grade">Grade the book:</label>
                                </div>
                                <select id="grade" name="grade" class="custom-select">
                                    <option value="" disabled selected>Choose...</option>`;
    for (i=5; i>0; i--){
        text += `                   <option value="${i}">${i}</option>`;
    }
    text += `                  </select>
                            </div>
                            <div class="col-12 form-group">
                                <label for="review">Review</label>
                                <textarea id="review" name="review" class="form-control" placeholder="Enter your review"></textarea>
                            </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-12 text-center">
                                    <button type="reset" class="btn btn-lg btn-red" onclick="cancelAddBook()">
                                        Cancel <i class="fas fa-times-circle"></i>
                                    </button>
                                    <button type="submit" class=" btn btn-lg btn-green">
                                        Add Book <i class="fas fa-plus-square"></i>
                                    </button>
                                </div>
                            </div>
                        
                        <div class="text-center mt-3">
                            <h4>More Book Information:</h4>
                        </div>
                        <div class="row">`;

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

function addBook(index){
    console.log(index, typeof(index));
    let book = search_result.items[index];
    console.log(book);
    bookToDocument(book);
}

function searchToDocument(){
    let text = `<div class="text-center m-5">
                    <h3>Search results:</h3>
                </div>`;
    
    if (search_result.totalItems==0){
        text += `<div class="text-center mt-3">No books found with the input given.</div>`;
    }
    else{
        let index = 0;
        text += `<div class="row">`;
        for (book of search_result.items){
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
                        text += `<img src=${book.volumeInfo.imageLinks.thumbnail}>`;
                    }
                }
       
                text += `<div class="card-text">`;
                if ("authors" in book.volumeInfo){
                    for (author of book.volumeInfo.authors){
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
                                Choose book
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
    window.location.href="#search_results";
}

function searchForBooks(title_or_author, search_text){
    if (!search_text || search_text.trim().length === 0){
        console.log("ingen info");
    }
    else{
        fetch("https://www.googleapis.com/books/v1/volumes?q="+ title_or_author + ":" + search_text + "&printType=books&projection=full&key=AIzaSyAa48h04CAMjJ1bVewMoBx-_8EZv1IBNpI")
        .then(res =>res.json())
        .then(res => {
            search_result = res;
            searchToDocument();
        })
        .catch(error => {
            console.log("something is wrong", error);
        });
    }
}

function searchTitle(group_names){
    category_groups = group_names;
    let search_title = $("#search_title").val();
    searchForBooks("intitle", search_title);
}

function searchAuthor(group_names){
    category_groups = group_names;
    let search_author = $("#search_author").val();
    searchForBooks("inauthor", search_author);
}

function addOpinion(book_id, title, called_from){
    $("#book_title").html(title);
    $("#hidden_input").html(`<input type="hidden" name="book_id" value="${book_id}">`);
    $('#modal').modal('show');
}

function selectToDocument(grade){
    text = ``;
    for (i=5; i>0; i--){
        if (i == Number(grade)){
            text += `<option value="${i}" selected>${i}</option>`;
        }
        else{
            text += `<option value="${i}">${i}</option>`;
        }
    }
    return text;
}

function changeOpinion(book_id, title, review_id, grade, review){
    $("#book_title").html(title);
    $('#modal_form').attr('action', '/change_opinion');
    $("#hidden_input").html(`<input type="hidden" name="book_id" value="${book_id}">
        <input type="hidden" name="review_id" value="${review_id}">`);
    $("#grade_m").html(selectToDocument(grade));
    $("#review_m").html(review)
    $('#modal').modal('show');
}