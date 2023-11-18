// dropdown para editar

document.addEventListener("DOMContentLoaded", function () {
  var dropForm = document.querySelectorAll(".drop-alterar");

  dropForm.forEach(function (form) {
    form.addEventListener("click", function () {
      var editForm = this.nextElementSibling;
      if (editForm.style.display === "block") {
        editForm.style.display = "none";
      } else {
        editForm.style.display = "block";
      }
    });
  });
});

// janela pop-up para editar

document.addEventListener("DOMContentLoaded", function () {
  var alterarForm = document.querySelectorAll(".alterar-tarefa");

  alterarForm.forEach(function (form) {
    form.addEventListener("click", function () {
      var janelaPopUp = form.nextElementSibling;
      janelaPopUp.style.display = "flex";
    });
  });

  window.addEventListener("click", function (event) {
    if (event.target.classList.contains("popup-bg")) {
      event.target.style.display = "none";
    }
  });
});
