$(document).ready(function() {
  // auto description
  $('#upload[type="file"]').change((e) => {
    var target = $('input[name*="description"]');
    var description = new Date().toISOString().slice(0, 10)+' '+e.target.files[0].name;
    if (target.val() == '') {
      target.val(description);
    }
  });

  $('#signout').click((e) => {
    $.post("/logout/")
     .done((data) => {
        window.location.replace("/");
     });
  });

  $('#change').click((e) => {
    // request to user as put method
    // change password to new one
  });

  // dropdown
  $('.dropdown-menu a.dropdown-item').click(function() {
    var type = $('input[name*="assignmentType"]');
    type.text($(this).text());
    type.val($(this).text());
  });

  // datepicker
  $('input[name*="date-from"]').datepicker({
    uiLibrary: 'bootstrap4',
    iconsLibrary: 'fontawesome',
    format: 'yyyy-mm-dd'
  });

  $('input[name*="date-to"]').datepicker({
    uiLibrary: 'bootstrap4',
    iconsLibrary: 'fontawesome',
    format: 'yyyy-mm-dd'
  });
});
