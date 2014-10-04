$(document).ready(function(){
  $.getJSON("./tu.json", function(data){

    data = _.sortBy(data, function(datum){ return datum.name;});
    _.forEach(data, function(datum){
      var $header = $("<h1>").text(datum.name[0]).appendTo("body");
      var $link = $("<a>").text(datum.url).attr('href', datum.url).insertAfter($header);
      var $text = $("<p>").text(datum.description).insertAfter($link);
      if (datum.dates[0]){
        var $price = $("<p>").text(datum.dates[0].price).insertAfter($text);
      }
    });
  });
});
