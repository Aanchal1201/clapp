$(document).ready(function () {
  $(".loader").hide();

  let inputFields = document.querySelectorAll(".inputElem");
  let cpass = document.getElementById("cpass");

  cpass.addEventListener("input", (e) => {
    checkBlank(cpass);
    if (cpass.value !== password.value) {
      cpass.parentElement.querySelector(".error").classList.remove("d-none");
      cpass.classList.add("errorInvalid");
    } else {
      cpass.parentElement.querySelector(".error").classList.add("d-none");
      cpass.classList.remove("errorInvalid");
    }
  });

  inputFields.forEach((elem) => {
    elem.addEventListener("input", (e) => {
      checkBlank(elem);
      errorCheck(elem, e);
      $(".userExist").addClass("d-none");
      $(".emailExist").addClass("d-none");
    });
  });

  function checkBlank(elem) {
    if (elem.value !== "") {
      elem.parentElement.querySelector("span").classList.add("notBlank");
    } else {
      elem.parentElement.querySelector("span").classList.remove("notBlank");
    }
  }
  function errorCheck(elem, e) {
    if (!e.target.checkValidity() || elem.value == "") {
      elem.parentElement.querySelector(".error").classList.remove("d-none");
      elem.classList.add("errorInvalid");
    } else {
      elem.parentElement.querySelector(".error").classList.add("d-none");
      elem.classList.remove("errorInvalid");
    }
  }

  $("#register").submit(function (event) {
    event.preventDefault();
  });
  document
    .querySelector(".inputBx input[type='submit']")
    .addEventListener("click", (e) => {
      e.preventDefault();
      let errors = document.querySelectorAll(".error");
      let isErrors = false;
      errors.forEach((err) => {
        if (
          err.parentElement.parentElement.querySelector("input").value == ""
        ) {
          err.parentElement.parentElement
            .querySelector("input")
            .classList.add("errorInvalid");
          err.classList.remove("d-none");
        }
        if (!err.classList.contains("d-none")) {
          isErrors = true;
        }
      });
      if (!isErrors) {
        $(".loader").show();
        $(".form").hide();
        $.ajax({
          type: "POST",
          url: "/account/validate_registration/",
          data: $("#register").serialize(),
          success: function (response) {
            if (response.success) {
              window.location.href = "/account/login";
            }
            if (response.userExist) {
              $(".userExist").removeClass("d-none");
            } else {
              $(".userExist").addClass("d-none");
            }
            if (response.emailExist) {
              $(".emailExist").removeClass("d-none");
            } else {
              $(".emailExist").addClass("d-none");
            }
            $(".loader").hide();
            $(".form").show();
            document.getElementById("password").value = "";
            document.getElementById("cpass").value = "";
          },
          error: function (error) {
            $("#message").html("Some error occured");
          },
        });
        return false;
      }
    });
});
