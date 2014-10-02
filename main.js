$(document).ready(function(){
  $.getJSON("./htw.json", function(data){
    _.forEach(data, function(datum){
      var $header = $("<h1>").text(datum.name[0]).appendTo("body");
      var $text = $("<p>").text(datum.description).insertAfter($header);
      if (datum.dates[0]){
        var $price = $("<p>").text(datum.dates[0].price).insertAfter($text);
      }
    });
  });
});
