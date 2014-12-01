(function(){
  "use strict";
  var app = angular.module("dashboard", []);
  app.controller("DashboardController" , function($scope, $http){
    $scope.serachTerm = "Kicker";
    $scope.bookable = "false";
    $scope.selection = [];
    $scope.lastUpdated = "";
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

    $http.get("http://localhost:5000/s/handball")
      .then(function(res){
        $scope.sportsClasses = res.data;
      });

    $http.get("http://localhost:5000/age")
      .then(function(res){
        $scope.lastUpdated = res.data;
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

        $http.get("http://localhost:5000/s/" + $scope.searchTerm, {params: parameters})
          .then(function(res){
            $scope.sportsClasses = res.data;
          });
      };
  });
})();
