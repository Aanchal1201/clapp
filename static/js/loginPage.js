$(document).ready(function () {
  $('.loader').hide();

  $("#login").submit(function (event) {
    event.preventDefault();
    $('.loader').show();
    $('.form').hide();
    $.ajax({
      type: "POST",
      url: "/account/validate_login/",
      data: $(this).serialize(),
      success: function (response) {
        if (response.success) {
          window.history.back();
        } else if (response.userNotExist) {
          $(".usernotExist").removeClass("d-none");
          $(".incorrectPass").addClass("d-none");
          document.getElementById("password-input").value = "";
        } else if (response.isPassIncorrect) {
          $(".usernotExist").addClass("d-none");
          $(".incorrectPass").removeClass("d-none");
          document.getElementById("password-input").value = "";
        }
        $('.loader').hide();
        $('.form').show();
      },
      error: function (error) {
        $("#message").html("Some error occured");
      },
    });
    return false;
  });
});
