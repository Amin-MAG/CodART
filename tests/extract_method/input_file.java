package com.company;

public class Main {

    public static void main(String[] args) {
        Student reza = new Student("97524698", "reza", 20);
        reza.actionNumberOne();
        reza.actionNumberTwo();
        reza.actionNumberThree();
        reza.actionNumberFour();
    }

}


class Student {
    private String studentId;
    private String name;
    private int age;

    public Student(String studentId, String name, int age) {
        this.studentId = studentId;
        this.name = name;
        this.age = age;
    }

    public void actionNumberOne() {
        this.name = "IUST_" + this.name;
        System.out.println("Student { " +
                "name: " + this.name + ", " +
                "age: " + this.age + ", " +
                "studentId: " + this.studentId + " }");
    }

    public void actionNumberTwo() {
        this.age = 32;
        System.out.println("Student { " +
                "name: " + this.name + ", " +
                "age: " + this.age + ", " +
                "studentId: " + this.studentId + " }");
    }

    public void actionNumberThree() {
        this.age += 3;
        System.out.println("Student { " +
                "name: " + this.name + ", " +
                "age: " + this.age + ", " +
                "studentId: " + this.studentId + " }");
    }

    public void actionNumberFour() {
        this.studentId = "97526312";
        System.out.println("Student { " +
                "name: " + this.name + ", " +
                "age: " + this.age + ", " +
                "studentId: " + this.studentId + " }");
    }

    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}