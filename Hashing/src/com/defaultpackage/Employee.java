package com.defaultpackage;

public class Employee {

    private String employeeId;

    Employee(String employeeId){
        this.employeeId = employeeId;
    }

    public String getEmployeeId(){
        return employeeId;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Employee)) return false;

        Employee employee = (Employee) o;

        return employeeId.equals(employee.employeeId);
    }

    @Override
    public int hashCode() {
        return employeeId.hashCode();
    }
}
