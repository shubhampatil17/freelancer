package org.project.travelmanagement.controllers;

import org.project.travelmanagement.entities.Trip;
import org.project.travelmanagement.services.interfaces.DatabaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
public class MainController {

    @Autowired
    DatabaseService databaseService;

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public String renderIndex() {
        return "homepage";
    }

    @RequestMapping(value = "/getTripList", method = RequestMethod.GET)
    @ResponseBody
    public List<Trip> getTripList() {
        List<Trip> trips = databaseService.findAllTrips();
        return trips;
    }

    @RequestMapping(value = "/getTripsByTransportation", method = RequestMethod.GET)
    @ResponseBody
    public List<Trip> getTripsByTransportation(@RequestParam(required = true) String mode) {
        List<Trip> trips = databaseService.findTripsByTransportationMode(mode);
        return trips;
    }

    @RequestMapping(value = "/addNewTrip", method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public Map<String, Object> addNewTrip(@RequestBody Trip trip) {
        Map<String, Object> response = new HashMap();
        try {
            databaseService.addNewTrip(trip);
            response.put("status", true);
            response.put("message", "Trip added successfully !");
        } catch (Exception e) {
            e.printStackTrace();
            response.put("status", false);
            response.put("message", "Error ! Invalid data.");
        }

        return response;
    }

    @RequestMapping(value = "/deleteTrip", method = RequestMethod.DELETE, produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public Map<String, Object> deleteTrip(@RequestParam(required = true) Long id) {
        Map<String, Object> response = new HashMap<>();
        try {
            databaseService.deleteTrip(id);
            response.put("status", true);
            response.put("message", "Trip deleted successfully !");
        } catch (Exception e) {
            e.printStackTrace();
            response.put("status", false);
            response.put("message", "Error ! Something went wrong.");
        }

        return response;
    }

    @RequestMapping(value = "/modifyTrip", method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public Map<String, Object> modifyTrip(@RequestBody Trip trip) {
        Map<String, Object> response = new HashMap<>();
        try {
            databaseService.modifyTrip(trip);
            response.put("status", true);
            response.put("message", "Trip modified successfully !");
        } catch (Exception e) {
            e.printStackTrace();
            response.put("status", false);
            response.put("message", "Error ! Invalid data.");
        }

        return response;
    }
}
