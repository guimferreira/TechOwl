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
