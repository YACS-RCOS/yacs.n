angular.module('yacs', [])
  .controller('schedule', ['$scope', '$http', function($scope, $http) {

    $scope.textSearch = ''
    $scope.departmentSearch = ''
    $scope.selectedSubsemester = ''
    $scope.classList = []

    $scope.subsemesterSearch = function (desiredSubsemester) {
      return function (subsemester) {
        if (desiredSubsemester) {
          return (desiredSubsemester.date_start.getTime() === subsemester.date_start.getTime() && desiredSubsemester.date_end.getTime() === subsemester.date_end.getTime())
        }
        return true
      }
    }

    // populate class list
    $http
      .get('/api/class')
      .then(res => {
        $scope.classList = res.data
        $scope.classList.forEach(course => {
          course.date_start = new Date(course.date_start)
          course.date_end = new Date(course.date_end)
        })
        console.log(res.data);
      })
      .catch(err => {
        console.error(err);
      })

    // populate filter fields
    // 1. departments
    $http
      .get('/api/department')
      .then(res => {
        $scope.departments = res.data.map(d => d.department)
        console.log($scope.departments)
      })
      .catch(err => {
        console.error(err)
      })

    // 1. date_range (sub_semesters) for classes
    $http
      .get('/api/subsemester')
      .then(res => {
        $scope.subsemesters = res.data
        $scope.subsemesters.forEach(subsemester => {
          subsemester.date_start = new Date(subsemester.date_start)
          subsemester.date_end = new Date(subsemester.date_end)
          subsemester.date_start_display = (subsemester.date_start.getMonth() + 1) + "/" + (subsemester.date_start.getDate() + 1)
          subsemester.date_end_display = (subsemester.date_end.getMonth() + 1) + "/" + (subsemester.date_end.getDate() + 1)
        })
        console.log($scope.subsemesters)
      })
      .catch(err => {
        console.error(err)
      })


    // sketch for sample code for scheduling
    $scope._schedule_template = {
      days: ['Mo', 'Tu', 'We', 'Th', 'Fr'],
      hours: [8,9,10,11,12,13,14,15,16,17,18,19,20]
    }

  }]);
