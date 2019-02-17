$("#ourform").submit(function(ev) {
  var chs = $("#chs").val();
  var len = $("#len").val();
  var temp = $("#temp").val();
  $.get("localhost:80/", {chords: chs, length: len, temperature: temp}, function(data) {
    alert(data);
  });
  alert("done");
});
