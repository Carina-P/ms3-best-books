$(document).ready(function(){
    $('.sidenav').sidenav({edge:"right"});
  });
  
$("#add_book").submit( () => {
    text = "Innan fetch";
    fetch("https://www.googleapis.com/books/v1/volumes?q=isbn:0747532699")
    .then(res =>res.json())
    .then(res => {
        console.log(res);
        console.log(description);
        text += res;
    })
    .catch(error => {
        console.log("something is wrong", error);
    });
    console.log("efter fetch");
    text += "Efter fetch";
    $("#result").html("här är det" + text);
});