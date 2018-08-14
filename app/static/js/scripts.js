$(document).ready(function(){
  // auto description
  $('#upload[type="file"]').change((e) => {
    var target = $('input[name="description"]');
    var description = new Date().toISOString().slice(0, 10)+' '+e.target.files[0].name;
    if (target.val() == '') {
      target.val(description);
    }
  });
});
