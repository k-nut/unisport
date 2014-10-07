$(document).ready(function(){
  $.getJSON("./alle.json", function(data){
    _.forEach(data, function(datum){
      if (_.some(datum.dates, function(date){ return true })){
        var $header = $("<h1>").text(datum.name[0]).appendTo("body");
        var $link = $("<a>").text(datum.url).attr('href', datum.url).insertAfter($header);
        var $text = $("<p>").text(datum.description).insertAfter($link);
        if (datum.dates[0]){
          var $price = $("<p>").text(datum.dates[0].price).insertAfter($text);
        }
        _.forEach(datum.dates, function(date){
          $("<p>").text(date.day).insertAfter($text);
        });
      };
    });
  });
});
