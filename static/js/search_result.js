// jshint esversion:6

// This HTML "back-link" is copied from
// https://stackoverflow.com/questions/8814472/how-to-make-an-html-back-link
// by https://stackoverflow.com/users/1495198/vivek-maharajh
let element = document.getElementById("back-link");
element.setAttribute("href", document.referrer);
/**
 * This function links user back to last page. And:
 * - Users get to hover over the link to see the URL
 * - Users don't end up with a corrupted back-stack
 */
element.onclick = function() {
  history.back();
  $('#flash-mess').html("");
  return false;
};