class Student{
    public String name;
    public int age;
    public String address;
    public int rollNo;

    public Student(String name, int age, String address, int rollNo){
        this.name = name;
        this.age = age;
        this.address = address;
        this.rollNo = rollNo;
    }

    public void details(){
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Address: " + address);
        System.out.println("Roll No: " + rollNo);
    }
    
}

class branch extends Student{
    public String branchName;
    public int branchCode;

    public branch(String name, int age, String address, int rollNo, String branchName, int branchCode){
        super(name, age, address, rollNo);
        this.branchName = branchName;
        this.branchCode = branchCode;
    }

    public void branchDetails(){
        System.out.println("Branch Name: " + branchName);
        System.out.println("Branch Code: " + branchCode);
    }
}

public class Inheritance{
    public static void main(String[] args){
        Student s = new Student("Bhavini", 20, "Gandhinagar", 39);
        s.details();
        System.out.println("...............");
        branch b = new branch("Bhavini", 20, "Gandhinagar", 39, "CSE", 1);
        b.branchDetails();
    }
}