package com.defaultpackage;

import static java.lang.Math.abs;

public class ClosedHashingWithLinearProbing implements HashingMethod {

    private static final int SIZE_OF_HASH_TABLE = 1000;
    private Employee[] hashTable = new Employee[SIZE_OF_HASH_TABLE];

    @Override
    public int primaryHashFunction(Employee employee) {
        return abs(employee.hashCode()) % SIZE_OF_HASH_TABLE;
    }

    @Override
    public void insertIntoHashTable(Employee employee){

        int initialHashIndex = primaryHashFunction(employee);
        int nextHashIndex = initialHashIndex;

        while(hashTable[nextHashIndex] != null){

            nextHashIndex = (nextHashIndex + 1) % SIZE_OF_HASH_TABLE;

            if(nextHashIndex == initialHashIndex){
                System.out.println("Skipping : Employee " + employee.getEmployeeId() + ". Hash table is full.");
                return;
            }
        }

        hashTable[nextHashIndex] = employee;
    }

    @Override
    public void searchEmployee(String employeeId) {

    	long startTime = System.nanoTime();
    	long endTime;

        int numberOfComparisons = 1;
        Employee employee = new Employee(employeeId);

        int initialHashIndex = primaryHashFunction(employee);
        int nextHashIndex = initialHashIndex;

        if (hashTable[nextHashIndex] == null){
            System.out.println("Employee " + employee.getEmployeeId() + " not found ! " +
                    numberOfComparisons + " comparison(s)");

            endTime = System.nanoTime();                
            System.out.println("Search Took : " + (endTime - startTime) + " nanoseconds.");
            return;
        }

        while( !(hashTable[nextHashIndex].equals(employee)) ){
            numberOfComparisons++;
            nextHashIndex = (nextHashIndex + 1) % SIZE_OF_HASH_TABLE;

            if((nextHashIndex == initialHashIndex) || (hashTable[nextHashIndex] == null)){
                System.out.println("Employee " + employee.getEmployeeId() + " not found ! " +
                numberOfComparisons + " comparison(s)");
                return;
            }
        }

        System.out.println("Employee " + employee.getEmployeeId() + " found ! " + numberOfComparisons + " comparison(s)");
        endTime = System.nanoTime();         
        System.out.println("Search Took : " + (endTime - startTime) + " nanoseconds.");
    }
}
