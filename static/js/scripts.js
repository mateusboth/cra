// let deleteBtn = document.querySelector(".confirm-delete");
// deleteBtn.addEventListener("click", ConfirmDelete)

function ConfirmDelete() {
    var isValid = confirm('Deseja deletar o calendário?');
    if (!isValid) { 
        event.preventDefault();}
    }
  
