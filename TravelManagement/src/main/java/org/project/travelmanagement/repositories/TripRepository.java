package org.project.travelmanagement.repositories;

import org.project.travelmanagement.entities.Trip;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface TripRepository extends CrudRepository<Trip, Long> {
    Trip findOne(Long id);

    List<Trip> findAll();

    List<Trip> findByTransportationIgnoreCase(String transportation);

    void deleteById(Long id);
}
