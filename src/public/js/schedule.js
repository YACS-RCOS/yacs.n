angular.module('yacs', [])
  .controller('schedule', ['$scope', '$http', function($scope, $http) {

    $scope.classList = []

    // populate class list
    $http
      .get('/api/class')
      .then(res => {
        $scope.classList = res.data
        console.log($scope.classList)
      })
      .catch(err => {
        console.error(err);
      })

    // sketch for sample code for scheduling
    $scope._schedule_template = {
      days: ['Mo', 'Tu', 'We', 'Th', 'Fr'],
      hours: [8,9,10,11,12,13,14,15,16,17,18,19,20]
    }

    // sample angular code
    $scope.sometext = "ues";
    $scope.classes = [
      {title: 'one'},
      {title: 'two'},
      {title: 'three'}
    ]

  }]);
