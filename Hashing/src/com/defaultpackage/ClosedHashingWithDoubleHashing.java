package com.defaultpackage;

import static java.lang.Math.abs;

public class ClosedHashingWithDoubleHashing implements HashingMethod {

    private static final int SIZE_OF_HASH_TABLE = 1000;
    private Employee[] hashTable = new Employee[SIZE_OF_HASH_TABLE];

    @Override
    public int primaryHashFunction(Employee employee) {
        return abs(employee.hashCode()) % SIZE_OF_HASH_TABLE;
    }

    @Override
    public void insertIntoHashTable(Employee employee) {

        int hashMultiplier = 1;

        int initialHashIndex = abs(primaryHashFunction(employee) + hashMultiplier*secondaryHashFunction(employee)) % SIZE_OF_HASH_TABLE;
        int nextHashIndex = initialHashIndex;

        while(hashTable[nextHashIndex] != null){
            hashMultiplier++;
            nextHashIndex = abs(primaryHashFunction(employee) + hashMultiplier*secondaryHashFunction(employee)) % SIZE_OF_HASH_TABLE;
        }

        hashTable[nextHashIndex] = employee;
    }

    @Override
    public void searchEmployee(String employeeId) {

    	long startTime = System.nanoTime();
    	long endTime;

        int numberOfComparisons = 1;
        int hashMultiplier = 1;

        Employee employee = new Employee(employeeId);

        int initialHashIndex = abs(primaryHashFunction(employee) + hashMultiplier*secondaryHashFunction(employee)) % SIZE_OF_HASH_TABLE;
        int nextHashIndex = initialHashIndex;

        if (hashTable[nextHashIndex] == null){
            System.out.println("Employee " + employee.getEmployeeId() + " not found ! " +
                    numberOfComparisons + " comparison(s)");
            return;
        }

        while( !(hashTable[nextHashIndex].equals(employee)) ){

            numberOfComparisons++;
            hashMultiplier++;

            nextHashIndex = abs(primaryHashFunction(employee) + hashMultiplier*secondaryHashFunction(employee)) % SIZE_OF_HASH_TABLE;

            if((nextHashIndex == initialHashIndex) || (hashTable[nextHashIndex] == null)){
                System.out.println("Employee " + employee.getEmployeeId() + " not found ! " +
                        numberOfComparisons + " comparison(s)");
                endTime = System.nanoTime();                
                System.out.println("Search Took : " + (endTime - startTime) + " nanoseconds.");
                return;
            }
        }

        System.out.println("Employee " + employee.getEmployeeId() + " found ! " + numberOfComparisons + " comparison(s)");
        endTime = System.nanoTime();                
        System.out.println("Search Took : " + (endTime - startTime) + " nanoseconds.");
    }

    public int secondaryHashFunction(Employee employee){
        return  997 - (employee.hashCode() % 997);
    }
}