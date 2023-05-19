class Employee{
    String name;
    String city;
    byte age;
    int salary;
    int phone;
    Employee(int phone){
        this.phone = phone;
    }

    public void write(){
        System.out.println("Name: "+name);
        System.out.println("City: "+city);
        System.out.println("Age: "+age);
        System.out.println("Salary: "+salary);
        System.out.println("Phone: "+phone);
    }

   
}

public class object_class{
    public static void main(String[] args) {
        Employee e1 = new Employee(12345);
        e1.name = "Rahul";
        e1.city = "Delhi";
        e1.age = 20;
        e1.salary = 20000;
        Employee e2 = new Employee(56789);
        e2.name = "Rohit";
        e2.city = "Mumbai";
        e2.age = 22;
        e2.salary = 35000;
        e1.write();
        e2.write();

    }
}