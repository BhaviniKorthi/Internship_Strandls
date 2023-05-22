import java.util.*;

public class ObjectClass {

    public boolean equals(Object obj) {
        return (this == obj);
    }

    public static void main(String[] args) {
        ObjectClass o1 = new ObjectClass();
        ObjectClass o2 = new ObjectClass();  
        Object x = new String("Hello");
        System.out.println(o1.toString());
        System.out.println(o1.hashCode());
        System.out.println(o1.equals(o2));
        System.out.println(o1.getClass());
        System.out.println(o1.getClass().getName());
        System.out.println(x.getClass().getName());
    }
}
