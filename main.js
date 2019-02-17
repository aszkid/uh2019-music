$("#ourform").submit(function(ev) {
  ev.preventDefault();
  var chs = $("#chs").val();
  var len = $("#len").val();
  var temp = $("#temp").val();
  $.get("http://localhost:80/gen", {chords: chs, length: len, temperature: temp}, function(data) {
    alert(data);
  });
});
