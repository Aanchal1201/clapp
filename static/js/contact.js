 let elems = document.querySelectorAll(".col1");
  elems.forEach(element => {

    element.addEventListener("input",(e)=>{
      if(!e.target.checkValidity() || element.value == ""){
        element.nextElementSibling.classList.remove("d-none")

      }
      else{
        element.nextElementSibling.classList.add("d-none")
      }
      
    })
  });

  document.querySelector("#contact").addEventListener("click",(e)=>{
    let errors = document.querySelectorAll("form .clearfix small")
    
    let err = false;
    errors.forEach(error=>{
      error.previousElementSibling.setAttribute("required","true")
      if(error.previousElementSibling.value == ""){
        error.classList.remove("d-none")
      }
      if(!error.classList.contains("d-none")){
        err = true
        e.preventDefault()
      }
    });
    if (!err){
      document.querySelector("#contact").submit()
    }
    
  })