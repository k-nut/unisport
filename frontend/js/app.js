(function(){
  "use strict";
  var BACKEND_URL = "//backend.unisport.berlin";
  var app = angular.module("dashboard", ['ngSanitize']);
  app.controller("DashboardController" , function($scope, $http, $sce, $timeout){
    $scope.searchTerm = "Handball";
    $scope.bookable = "false";
    $scope.selection = [];
    $scope.lastUpdated = "";
    $scope.numberOfResults = -1;
    $scope.days = [{day: "Mo", checked: false},
      {day: "Di", checked: false},
      {day: "Mi", checked: false},
      {day: "Do", checked: false},
      {day: "Fr", checked: false},
      {day: "Sa", checked: false},
      {day: "So", checked: false}
    ];
    $scope.$watch("selection", function () {
      angular.forEach($scope.selection, function (value, index) {
        $scope.days[index].checked = value;
      });
    }, true);

    $http.get(BACKEND_URL + "/classes?name=handball").then(displayResults);

    $http.get(BACKEND_URL + "/age")
    .then(function(res){
      $scope.lastUpdated = moment(res.data).format("YYYY-MM-DD hh:mm");
    });

    $scope.searchClasses = function(){
      var parameters = {};
      if ($scope.bookable !== "false"){
        parameters.bookable = $scope.bookable;
      }
      var checkedDays = _.filter($scope.days, function(day){
        return day.checked === true;
      }).map(function(day) { return day.day;});
      if (checkedDays.length > 0){
        parameters.days = checkedDays.join(",");
      }

      if ($scope.searchTerm !== ""){
        parameters.name = $scope.searchTerm;
      }

      $scope.loading = true;
      $http.get(BACKEND_URL + "/classes", {params: parameters}).then(displayResults);
    }

    function displayResults(results){
      if ($scope.searchTerm){
        _.forEach(results.data, function(datum){
          datum.description = $sce.trustAsHtml(datum.description.replace(new RegExp("(" + $scope.searchTerm + ")", "gi"), "<span class='highlight'>$1</span>"));
        });
      }
      $scope.sportsClasses = results.data;
      $scope.numberOfResults = results.data.length;
      $scope.loading = false;
      $timeout(function(){$(".collapse:first").collapse()}, 500);
    }
  });
})();
