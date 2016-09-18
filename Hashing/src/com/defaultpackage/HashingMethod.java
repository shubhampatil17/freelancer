package com.defaultpackage;

public interface HashingMethod {

    int primaryHashFunction(Employee employee);
    void insertIntoHashTable(Employee employee);
    void searchEmployee(String employeeId);
}
