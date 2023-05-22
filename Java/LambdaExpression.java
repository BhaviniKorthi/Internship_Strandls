import java.util.*;

interface Lambda {
    String print(String n);
}

public class LambdaExpression {

    public static void main(String[] args){
        ArrayList<Integer> arr = new ArrayList<Integer>();
        arr.add(1);
        arr.add(2);
        arr.add(3);
        arr.add(4);
        arr.add(5);
        //type1
        arr.forEach(n -> System.out.println(n));
        //type2
        Lambda l = (t) -> t + " World";
        System.out.println(l.print("Hello"));
        
    }
    
}
