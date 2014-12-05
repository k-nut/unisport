(function(){
  "use strict";
  var app = angular.module("dashboard", ['ngSanitize']);
  app.controller("DashboardController" , function($scope, $http, $sce){
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

    $http.get("http://localhost:5000/s/handball")
      .then(function(res){
        if ($scope.searchTerm){
          _.forEach(res.data, function(datum){
            datum.description = $sce.trustAsHtml(datum.description.replace(new RegExp("(" + $scope.searchTerm + ")", "gi"), "<span class='highlight'>$1</span>"));
          });
        }
        $scope.sportsClasses = res.data;
        setTimeout(function(){$(".collapse:first").collapse()}, 500);
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

          $scope.loading = true;
          $http.get("http://localhost:5000/s/" + $scope.searchTerm, {params: parameters})
            .then(function(res){
              if ($scope.searchTerm){
                _.forEach(res.data, function(datum){
                  datum.description = $sce.trustAsHtml(datum.description.replace(new RegExp("(" + $scope.searchTerm + ")", "gi"), "<span class='highlight'>$1</span>"));
                });
              }
              $scope.sportsClasses = res.data;
              $scope.numberOfResults = res.data.length;
              $scope.loading = false;
            });
        };
  });
})();
