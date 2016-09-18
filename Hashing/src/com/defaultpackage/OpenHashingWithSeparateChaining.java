package com.defaultpackage;

import java.util.LinkedList;
import static java.lang.Math.abs;

public class OpenHashingWithSeparateChaining implements HashingMethod {

    private static final int SIZE_OF_HASH_TABLE = 1000;
    private LinkedList<Employee>[] hashTable = new LinkedList[SIZE_OF_HASH_TABLE];

    OpenHashingWithSeparateChaining(){
        for(int i=0 ; i < SIZE_OF_HASH_TABLE ; i++){
            hashTable[i] = new LinkedList<Employee>();
        }
    }

    @Override
    public int primaryHashFunction(Employee employee) {
        return abs(employee.hashCode()) % SIZE_OF_HASH_TABLE;
    }

    @Override
    public void insertIntoHashTable(Employee employee) {
        int hashIndex = primaryHashFunction(employee);
        hashTable[hashIndex].add(employee);
    }

    @Override
    public void searchEmployee(String employeeId) {

    	long startTime = System.nanoTime();
    	long endTime;
    	

        Employee employee = new Employee(employeeId);
        int hashIndex = primaryHashFunction(employee);
        int numberOfComparisons = 1;

        LinkedList<Employee> employees = hashTable[hashIndex];

        for(Employee e : employees){

            if(e.equals(employee)){
                System.out.println("Employee " + employee.getEmployeeId() + " found ! " +
                        numberOfComparisons + " comparison(s)");

                endTime = System.nanoTime();               
                System.out.println("Search Took : " + (endTime - startTime) + " nanoseconds.");
                return;
            }

            numberOfComparisons++;
        }

        System.out.println("Employee " + employee.getEmployeeId() + " not found ! " +
                numberOfComparisons + " comparison(s)");

        endTime = System.nanoTime();                
        System.out.println("Search Took : " + (endTime - startTime) + " nanoseconds.");
    }
}
