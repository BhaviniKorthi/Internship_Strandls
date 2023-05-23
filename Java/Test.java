import java.util.Objects;
class ObjClass{
    int age;
    String name;

    public String toString(){
        return "Name: " + name + " Age: " + age;
    }
}

public class Test {
    
    public static void main(String[] args){
        ObjClass obj = new ObjClass();
        obj.age = 20;
        obj.name = "John";
        System.out.println(Objects.hash(obj.name, obj.age));
        System.out.println(obj.hashCode());
    }    
}
