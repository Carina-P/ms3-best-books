let books = [];

$(document).ready(function(){
    $('.sidenav').sidenav({edge:"right"});
    $('select').formSelect();
});

function addBook(index){
    console.log(index, typeof(index));
}

function resultToDocument(result){
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
        fetch("https://www.googleapis.com/books/v1/volumes?q="+ title_or_author + ":" + search_text + "&printType=books&projection=lite&key=AIzaSyAa48h04CAMjJ1bVewMoBx-_8EZv1IBNpI")
        .then(res =>res.json())
        .then(res => {
            console.log(res);
            books = res.items;
            console.log(books);
            resultToDocument(res);
        })
        .catch(error => {
            console.log("something is wrong", error);
        });
    }
}

function searchTitle(){
    console.log("Sök title");
    let search_title = $("#search_title").val();
    searchForBooks("intitle", search_title);
}

function searchAuthor(){
    console.log("Sök författare");
    let search_author = $("#search_author").val();
    searchForBooks("inauthor", search_author);
}