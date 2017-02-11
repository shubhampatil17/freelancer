package org.project.travelmanagement.services.implementations;

import org.project.travelmanagement.entities.Trip;
import org.project.travelmanagement.repositories.TripRepository;
import org.project.travelmanagement.services.interfaces.DatabaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@Component
public class DatabaseServiceImpl implements DatabaseService {

    @Autowired
    private TripRepository tripRepository;

    @Override
    public List<Trip> findAllTrips() {
        return tripRepository.findAll();
    }

    @Override
    public List<Trip> findTripsByTransportationMode(String transportation) {
        return tripRepository.findByTransportationIgnoreCase(transportation);
    }

    @Override
    @Transactional
    public void deleteTrip(Long id) {
        tripRepository.deleteById(id);
    }

    @Override
    public void modifyTrip(Trip newTrip) {
        try {
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
            Date startDate = simpleDateFormat.parse(newTrip.getStartDate());
            Date endDate = simpleDateFormat.parse(newTrip.getEndDate());

            if (endDate.after(startDate)) {
                Trip oldTrip = tripRepository.findOne(newTrip.getId());
                oldTrip.setName(newTrip.getName());
                oldTrip.setLocation(newTrip.getLocation());
                oldTrip.setStartDate(newTrip.getStartDate());
                oldTrip.setEndDate(newTrip.getEndDate());
                oldTrip.setTransportation(newTrip.getTransportation());
                tripRepository.save(oldTrip);
            } else {
                throw new IllegalArgumentException("Illegal Dates");
            }

        } catch (Exception e) {
            e.printStackTrace();
            throw new IllegalArgumentException(e.getMessage());
        }
    }

    @Override
    public void addNewTrip(Trip trip) throws IllegalArgumentException {
        try {
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
            Date startDate = simpleDateFormat.parse(trip.getStartDate());
            Date endDate = simpleDateFormat.parse(trip.getEndDate());

            if (endDate.after(startDate)) {
                tripRepository.save(trip);
            } else {
                throw new IllegalArgumentException("Illegal Dates");
            }

        } catch (Exception e) {
            e.printStackTrace();
            throw new IllegalArgumentException(e.getMessage());
        }
    }
}
