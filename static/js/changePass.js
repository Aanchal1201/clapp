$('.loader').hide();
function checkBlank(elem) {
     if (elem.value !== "") {
       elem.parentElement.querySelector("span").classList.add("notBlank");
     }
     else {
       elem.parentElement.querySelector("span").classList.remove("notBlank");
     }
   }

   document.querySelectorAll(".inputElem").forEach(elem=>{
     elem.addEventListener("input",()=>{
       checkBlank(elem);
       
     })
   })

   let cpass = document.querySelector("#cpass")
   let password = document.querySelector("#password")
   password.addEventListener("input",(e)=>{
     if (!e.target.checkValidity() || password.value == "") {
       password.parentElement.querySelector(".error").classList.remove("d-none")
       password.classList.add("errorInvalid")
     }
     else {
       password.parentElement.querySelector(".error").classList.add("d-none");
       password.classList.remove("errorInvalid")
     }
   })

   cpass.addEventListener("input", (e) => {
     if (cpass.value !== password.value) {
       cpass.parentElement.querySelector(".error").classList.remove("d-none")
       cpass.classList.add("errorInvalid")
     }
     else {
       cpass.parentElement.querySelector(".error").classList.add("d-none")
       cpass.classList.remove("errorInvalid")
     }
   })

   $("#changePass").submit(function (event) {
   event.preventDefault();
   $('.loader').show();
   $('.form').hide();
   $.ajax({
     type: "POST",
     url: "/account/validate_change_password/",
     data: $(this).serialize(),
     success: function (response) {
       if (response.success) {
         document.querySelector(".incorrectPass").classList.add("d-none")
         $("#message").html("Password change successfully");
         window.setTimeout(()=>{
          window.location.href="/"; 
         }, 1000)
         
       }
       else{
         document.querySelector(".incorrectPass").classList.remove("d-none")
       }
       $('.loader').hide();
       $('.form').show();
       emptyFields()
     },
     error: function (error) {
       $("#message").html("Some error occured");
     },
   });
   return false;
 });

 function emptyFields(){
   document.querySelectorAll(".inputElem").forEach(elem=>{
     elem.value = "";
   })
 }