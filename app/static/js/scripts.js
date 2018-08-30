$(document).ready(function() {
  // modal edit mode
  $('#challengeModal').on('shown.bs.modal', () => {
    var btn = $('button[data-target*="#challengeModal"]');
    if (btn.data('mode') == 'Edit') {
      $('input[name*="challengeTitle"]').val($('#challengeTitle').text());
      // TODO: reload date, files
    }
  });

  // auto description
  $('#upload[type="file"]').change((e) => {
    var target = $('input[name*="description"]');
    var description = new Date().toISOString().slice(0, 10)+' '+e.target.files[0].name;
    if (target.val() == '') {
      target.val(description);
    }
  });

  // change password, singout
  $('#change').click((e) => {
    $.ajax({
      url: '/user/',
      dataType: 'json',
      method: 'PUT',
      headers: { "Content-Type": "application/json" },
      data: JSON.stringify({
        'old': $('input[name*="oldPassword"]').val(),
        'new': $('input[name*="newPassword"]').val()
      }), success: (r) => {
        if (r.status == "ok") {
          $('#signout').trigger('click');
        } else {
          var target = $('input[name*="oldPassword"]');
          if (!target.hasClass('is-invalid'))
            target.addClass('is-invalid');
        }
      }
    });
  });
  $('#signout').click((e) => {
    $.post("/logout/")
     .done((data) => {
        window.location.replace("/");
     });
  });

  // dropdown
  $('.dropdown-menu a.dropdown-item').click(function() {
    var type = $('input[name*="challengeType"]');
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
