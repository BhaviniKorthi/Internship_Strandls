import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;

public class Collections_ {

    public static void main(String[] args){
        ArrayList<Integer> list = new ArrayList<Integer>();
        HashMap<String, String> hmap = new HashMap<String, String>();
        HashSet<String> hset = new HashSet<String>();
        list.add(1);
        list.add(3);
        list.add(2);
        hmap.put("A", "a");
        hmap.put("B", "b");
        hmap.put("C", "c");
        hset.add("A");
        hset.add("A");
        hset.add("A");

        Collections.sort(list); //
        System.out.println("...........Arraylist..........");
        for (int i: list){
            System.out.println(i);
        }
        System.out.println("...........HashMap.........."); 
        System.out.println("keys:"+ hmap.keySet());
        System.out.println("values:"+ hmap.values());
        System.out.println("key-value pairs:"+ hmap.entrySet());
        for (String i: hmap.keySet()){
            System.out.println("key:"+ i + " value:"+ hmap.get(i));
        }
        System.out.println("...........HashSet..........");
        System.out.println("HashSet:"+ hset);
        System.out.println("HashSet size:"+ hset.size());
    }
    
}
