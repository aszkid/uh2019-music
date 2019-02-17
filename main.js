$("#ourform").submit(function(ev) {
  ev.preventDefault();
  var chs = $("#chs").val();
  var len = $("#len").val();
  var temp = $("#temp").val();
  // $.getJSON("http://localhost:80/gen", {chords: chs, length: len, temperature: temp}, function(data) {
  //   alert('godd');
  // });
   $.ajax ({
    type: 'GET',
    url: 'localhost:80/gen',
    data: JSON.stringify({chords: chs, length: len, temperature: temp}),
    dataType: "json",
    contentType: "text/plain",
    success: function (data) {
        // Success callback
        alert(data);
    },
    error: function() {
        //any error to be handled
        alert("bad!");
    }
 });
});
