var app = angular.module("travelManagement", []).controller("mainController", function ($scope, $http, $timeout) {

    $scope.tripData = {};
    $scope.tripData.transportation = "Boat";

    $scope.getTripList = function () {
        $http({
            method: 'GET',
            url: '/getTripList'
        }).then(function (response) {
            $scope.tripList = response.data;
        }, function (error) {
            console.log(error);
        })
    }

    $scope.getTripsByBoat = function () {
        $http({
            method: 'GET',
            url: '/getTripsByTransportation',
            params: {
                'mode': 'boat'
            }
        }).then(function (response) {
            $scope.tripsByBoat = response.data;
        }, function (error) {
            console.log(error);
        })
    }

    $scope.getTripsByPlane = function () {
        $http({
            method: 'GET',
            url: '/getTripsByTransportation',
            params: {
                'mode': 'plane'
            }
        }).then(function (response) {
            $scope.tripsByPlane = response.data;
        }, function (error) {
            console.log(error);
        })
    }

    $scope.getTripsByCar = function () {
        $http({
            method: 'GET',
            url: '/getTripsByTransportation',
            params: {
                'mode': 'car'
            }
        }).then(function (response) {
            $scope.tripsByCar = response.data;
        }, function (error) {
            console.log(error);
        })
    }

    $scope.parseDate = function (dateString) {
        var date = new Date(dateString);
        return date.toLocaleDateString();
    }

    $scope.addNewTrip = function () {
        $scope.addTripBtnDisabled = true;
        $http({
            method: 'POST',
            url: '/addNewTrip',
            data: {
                'name': $scope.tripData.name,
                'location': $scope.tripData.location,
                'startDate': $scope.tripData.startDate,
                'endDate': $scope.tripData.endDate,
                'transportation': $scope.tripData.transportation
            }
        }).then(function (response) {
            $scope.addTripComplete = true;
            $scope.addTripBtnDisabled = false;
            $scope.addTripMessage = response.data.message;
            if (response.data.status) {
                $scope.addTripSuccess = true;
                $scope.getTripList()
                $scope.getTripsByBoat();
                $scope.getTripsByPlane();
                $scope.getTripsByCar();
                $timeout(function () {
                    $scope.tripData = {}
                    $scope.tripData.transportation = "Boat";
                    $('#addTripModal').modal('hide');
                    $scope.addTripComplete = false;
                }, 2000);
            } else {
                $scope.addTripSuccess = false;
            }

        }, function (error) {
            $scope.addTripBtnDisabled = false;
            console.log(error);
        })
    }

    $scope.popUpDeleteConfirmation = function (id) {
        $('#deleteTripConfirmation').modal('show');
        $scope.tripIdTodelete = id;
    }

    $scope.deleteTrip = function () {
        $http({
            method: 'DELETE',
            url: '/deleteTrip',
            params: {
                'id': $scope.tripIdTodelete
            }
        }).then(function (response) {
            $scope.deleteTripComplete = true;
            $scope.deleteTripMessage = response.data.message;
            if (response.data.status) {
                $scope.deleteTripSuccess = true;
                $scope.getTripList()
                $scope.getTripsByBoat();
                $scope.getTripsByPlane();
                $scope.getTripsByCar();
                $timeout(function () {
                    $scope.tripIdTodelete = undefined;
                    $('#deleteTripConfirmation').modal('hide');
                    $scope.deleteTripComplete = false;
                }, 2000)
            } else {
                $scope.deleteTripSuccess = false;
            }

        }, function (error) {
            console.log(error);
        })
    }


    $scope.getDateObject = function (dateString) {
        return new Date(dateString);
    }

    $scope.popUpModifyTripModal = function (trip) {
        $scope.tripData.id = trip.id;
        $scope.tripData.name = trip.name;
        $scope.tripData.location = trip.location;
        $scope.tripData.startDate = $scope.getDateObject(trip.startDate);
        $scope.tripData.endDate = $scope.getDateObject(trip.endDate);
        $scope.tripData.transportation = trip.transportation;

        $('#modifyTripModal').modal('show');
    }

    $scope.modifyTrip = function () {
        $http({
            method: 'POST',
            url: '/modifyTrip',
            data: {
                'id': $scope.tripData.id,
                'name': $scope.tripData.name,
                'location': $scope.tripData.location,
                'startDate': $scope.tripData.startDate,
                'endDate': $scope.tripData.endDate,
                'transportation': $scope.tripData.transportation
            }
        }).then(function (response) {
            $scope.modifyTripComplete = true;
            $scope.modifyTripMessage = response.data.message;
            if (response.data.status) {
                $scope.modifyTripSuccess = true;
                $scope.getTripList()
                $scope.getTripsByBoat();
                $scope.getTripsByPlane();
                $scope.getTripsByCar();
                $timeout(function () {
                    $scope.tripData = {}
                    $scope.tripData.transportation = "Boat";
                    $('#modifyTripModal').modal('hide');
                    $scope.modifyTripComplete = false;
                }, 2000);
            } else {
                $scope.modifyTripSuccess = false;
            }

        }, function (error) {
            console.log(error);
        })
    }


    $scope.getTripList()
    $scope.getTripsByBoat();
    $scope.getTripsByPlane();
    $scope.getTripsByCar();

});