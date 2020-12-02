$(document).ready(function(){
    $('.sidenav').sidenav({edge:"right"});
});

function searchTitle(){
    console.log("Sök title");
    let title = $("#search_txt").val();

    if (!title || title.trim().length === 0){
        console.log("ingen info");
    }
    else{
        console.log(title);
        fetch("https://www.googleapis.com/books/v1/volumes?q=intitle:"+ title+"&printType=books&projection=full&key=AIzaSyAa48h04CAMjJ1bVewMoBx-_8EZv1IBNpI")
        .then(res =>res.json())
        .then(res => {
            console.log(res);
        })
        .catch(error => {
            console.log("something is wrong", error);
        });
    }
}

function searchAuthor(){
    console.log("Sök författare");
    let author = $("#search_txt").val();

    if (!author || author.trim().length === 0){
        console.log("ingen info");
    }
    else{
        console.log(title);
        fetch("https://www.googleapis.com/books/v1/volumes?q=intitle:"+ author+"&printType=books&projection=lite&key=AIzaSyAa48h04CAMjJ1bVewMoBx-_8EZv1IBNpI")
        .then(res =>res.json())
        .then(res => {
            console.log(res);
        })
        .catch(error => {
            console.log("something is wrong", error);
        });
    }
}