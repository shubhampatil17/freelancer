package org.project.travelmanagement.services.interfaces;

import org.project.travelmanagement.entities.Trip;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface DatabaseService {
    List<Trip> findAllTrips();

    List<Trip> findTripsByTransportationMode(String transportation);

    void addNewTrip(Trip trip) throws Exception;

    void deleteTrip(Long id);

    void modifyTrip(Trip newTrip);
}
