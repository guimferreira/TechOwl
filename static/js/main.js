// addEventListener -
// DOMContentLoaded
// querySelectorAll - retorna uma lista de elementos (Nodelist) presente no documento que coincida com o seletor especificado
// forEach - metódo que chama a função para cada elemento na lista
// Element.nextElementSibling - propriedade que retorna o elemento que se encontra logo após o especificado

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
