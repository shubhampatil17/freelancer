package com.defaultpackage;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.Scanner;

public class Application {

    private Scanner scanner;
    private File file;
    private FileReader fileReader;
    private int sizeOfDataset;
    private String datasetName;
    private HashingMethod hashingMethod;

    Application(){
        scanner = new Scanner(System.in);
    }

    public void start(){
        System.out.println("Starting application .... ");

        try{
            selectDataset();
            setHashingMethod();
            readDatasetAndPopulateHashTable();
            searchForKeyInHashTable();

        }catch (Exception e){
            System.out.println(e.getMessage());
            System.exit(1);
        }
    }

    private void setHashingMethod(){

        System.out.println("Select a Hashing Method :");
        System.out.println("1. Open Hashing with Separate Chaining :");
        System.out.println("2. Closed Hashing with Linear Probing :");
        System.out.println("3. Closed Hashing with Double Hashing :");
        System.out.println("Input :");

        int choice = scanner.nextInt();

        getHashingMethodBasedOnNumber(choice);
    }

    private void getHashingMethodBasedOnNumber(int choice){

        switch (choice){
            case 1:
                hashingMethod = new OpenHashingWithSeparateChaining();
                break;

            case 2:
                hashingMethod = new ClosedHashingWithLinearProbing();
                break;

            case 3:
                hashingMethod = new ClosedHashingWithDoubleHashing();
                break;

            default:
                throw new IllegalArgumentException("Invalid Choice !");
        }
    }

    private void selectDataset() throws Exception {
    	
    	System.out.println("Select a dataset.");
    	System.out.println("1. Dataset100.txt");
    	System.out.println("2. Dataset300.txt");
    	System.out.println("3. Dataset500.txt");
    	System.out.println("4. Dataset700.txt");
    	System.out.println("5. Dataset900.txt");
    	System.out.println("Input :");
    	
    	int choice = scanner.nextInt();
    	
    	switch(choice){
    	case 1: 
    		datasetName = "Dataset100.txt";
    		sizeOfDataset = 100;
    		break;
    		
    	case 2: 
    		datasetName = "Dataset300.txt";
    		sizeOfDataset = 300;
    		break;
    		
    	case 3: 
    		datasetName = "Dataset500.txt";
    		sizeOfDataset = 500;
    		break;
    		
    	case 4: 
    		datasetName = "Dataset700.txt";
    		sizeOfDataset = 700;
    		break;
    		
    	case 5: 
    		datasetName = "Dataset900.txt";
    		sizeOfDataset = 900;
    		break;
    		
    	default:
    		throw new IllegalArgumentException("Invalid choice !");
    	}

        file = new File(datasetName);

        try{
            if(!file.exists()){
                file.createNewFile();
            }

            fileReader = new FileReader(file);

        }catch (Exception e){
            System.out.println(e.getMessage());
            System.exit(1);
        }
    }

    private void readDatasetAndPopulateHashTable() throws Exception{

    	
    	
        BufferedReader bufferedReader = new BufferedReader(fileReader);

        for(int i=0; i < sizeOfDataset; i++){
            String employeeId = bufferedReader.readLine();
            Employee employee = new Employee(employeeId);
            hashingMethod.insertIntoHashTable(employee);
        }

        System.out.println("Hash Table populated successfully !");

        bufferedReader.close();
        fileReader.close();
    }

    private void searchForKeyInHashTable(){

        boolean continueLooping = true;

        while (continueLooping){

            System.out.println("Enter an employee from " + datasetName +" to search.");
            System.out.println("Or enter 'stop' to stop application.");
            String employeeId = scanner.next();

            switch (employeeId){
                case "stop" :
                    continueLooping = false;
                    break;

                default:
                    hashingMethod.searchEmployee(employeeId);
                    break;
            }
        }
    }
}
