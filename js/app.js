(function(){
  "use strict";
  var app = angular.module("dashboard", []);
  app.controller("DashboardController" , function($scope, $http){
    $scope.serachTerm = "Kicker";
    $scope.bookable = "false";

    $http.get("http://localhost:5000/s/handball")
      .then(function(res){
        $scope.sportsClasses = res.data;
      });

      $scope.searchClasses = function(){
        var parameters = {};
        if ($scope.bookable !== "false"){
          parameters.bookable = $scope.bookable;
        }
        $http.get("http://localhost:5000/s/" + $scope.searchTerm, {params: parameters})
          .then(function(res){
            $scope.sportsClasses = res.data;
          });
      };
  });
})();
