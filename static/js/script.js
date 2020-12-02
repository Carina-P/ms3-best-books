$(document).ready(function(){
    $('.sidenav').sidenav({edge:"right"});
});

function resultToDocument(result){
    let text = `<div class="center-align">
                <h3>Search results:</h3>
            </div>`;
    
    if (result.totalItems==0){
        text += `<div>No books found with the input given.</div>`;
    }
    else{
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
                            <a href="#" class="btn-small bgr-red txt-ligth dark-shadow">Add book to this site</a>
                        </div>    
                    </div>
                </div>`;
            }
        }
    }
    $("#search_results").html(text);
}

function searchForBooks(title_or_author){
    let search_text = $("#search_txt").val();

    if (!search_text || search_text.trim().length === 0){
        console.log("ingen info");
    }
    else{
        console.log(search_text);
        fetch("https://www.googleapis.com/books/v1/volumes?q="+ title_or_author + ":" + search_text + "&printType=books&projection=lite&key=AIzaSyAa48h04CAMjJ1bVewMoBx-_8EZv1IBNpI")
        .then(res =>res.json())
        .then(res => {
            console.log(res);
            resultToDocument(res);
        })
        .catch(error => {
            console.log("something is wrong", error);
        });
    }
}

function searchTitle(){
    console.log("Sök title");
    searchForBooks("intitle");
}

function searchAuthor(){
    console.log("Sök författare");
    searchForBooks("inauthor");
}