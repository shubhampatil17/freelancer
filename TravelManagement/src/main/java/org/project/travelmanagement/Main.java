package org.project.travelmanagement;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.project.travelmanagement.entities.Trip;
import org.project.travelmanagement.services.interfaces.DatabaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.ResourceLoader;

import java.util.List;

@SpringBootApplication
public class Main implements CommandLineRunner {

    @Autowired
    ResourceLoader resourceLoader;

    @Autowired
    DatabaseService databaseService;

    @Override
    public void run(String... strings) throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();
        List<Trip> preloadedTrips = objectMapper.readValue(new ClassPathResource("preloadedTrips.json").getFile(), new TypeReference<List<Trip>>() {
        });

        for (Trip trip : preloadedTrips) {
            try {
                databaseService.addNewTrip(trip);
            } catch (IllegalArgumentException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }
}
