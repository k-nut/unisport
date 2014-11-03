(function(){
  'use strict';
  var app = angular.module('dashboard', []);
  app.controller('DashboardController' , function($scope, $http){
    $http.get('/json/alle.json')
    .then(function(res){
      $scope.sportsClasses = res.data;
    });
    $scope.startsWithA = function(sportsClass){
      return sportsClass.name.startsWith("A");
    };
  });
})();
