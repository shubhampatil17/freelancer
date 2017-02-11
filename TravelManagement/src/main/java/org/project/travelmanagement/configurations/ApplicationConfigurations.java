package org.project.travelmanagement.configurations;

import com.google.gson.Gson;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ApplicationConfigurations {

    @Bean
    Gson gson() {
        return new Gson();
    }
}
