$(document).ready(function () {
  var fav = document.createElement("link");
  fav.rel = "shortcut icon";
  fav.href = "../static/login.svg";
  fav.type = "image/x-icon";
  document.head.appendChild(fav);
  $("#username").on("blur", function () {
    if ($("#username").val() === "") {
      $(".err").html("username required");
    }
  });
  $("#password").on("blur", function () {
    if ($("#username").val() === "") {
      $(".err").html("password needed");
    }
  });
});
