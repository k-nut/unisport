(function(){
  "use strict";
  var app = angular.module("dashboard", []);
  app.controller("DashboardController" , function($scope, $http){
  $scope.serachTerm = "Kicker";

    $http.get("http://localhost:5000/s/kicker")
    .then(function(res){
      $scope.sportsClasses = res.data;
    });

    $scope.searchClasses = function(){
      $http.get("http://localhost:5000/s/" + $scope.searchTerm)
        .then(function(res){
          $scope.sportsClasses = res.data;
        });
    };
  });
})();
