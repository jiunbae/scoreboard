function updateRankBoard(role) {
  console.log('update rank' + role);
  var boxes = $($('.rank-checkbox').get().reverse());
  boxes.each((i, r) => {
    let val = Math.pow(2, boxes.length - i - 1);
    if (role >= val) {
      role -= val;
    } else {
      $(r).prop('checked', 'true');
    }
  });
}

$(document).ready(function() {
  // modal edit mode
  $('#challengeModal').on('shown.bs.modal', () => {
    var btn = $('button[data-target*="#challengeModal"]');
    if (btn.data('mode') == 'Edit') {
      $('input[name*="challengeTitle"]').val($('#challengeTitle').text());
      // TODO: reload date, files
    }
  });

  // rank board attribute 
  if ($('#rankboard').length) {
    updateRankBoard($('#rankboard').data('rank-checkbox'));
  };
  $('.rank-checkbox').change(function(e) {
    var id = $('#rankboard').data('id');
    var boxes = $('.rank-checkbox');
    var val = (boxes.index($(this))+1) * ($(this).is(':checked') ? -1 : 1);

    $.ajax({
      url: '/challenge/' + String(id),
      dataType: 'json',
      method: 'PUT',
      headers: { "Content-Type": "application/json" },
      data: JSON.stringify({
        'board_role': val
      }), success: (r) => {
        console.log(val);
        updateRankBoard(r.board_role);
        console.log(r.board_role);
      }
    });
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
