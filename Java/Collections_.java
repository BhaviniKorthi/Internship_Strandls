import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;

public class Collections_ {

    public static void main(String[] args) {
        ArrayList<Integer> list = new ArrayList<Integer>();
        list.add(1);
        list.add(3);
        list.add(2);

        Collections.sort(list);
        System.out.println("...........ArrayList..........");
        for (int i : list) {
            System.out.println(i);
        }

        System.out.println(("...........Iterator.........."));
        Iterator<Integer> itr = list.iterator();
        while (itr.hasNext()) {
            int t = itr.next();
            System.out.println(t);
            if (t == 2) {
                itr.remove();
            }
        }
        System.out.println("After removing 2: " + list);

        HashMap<String, String> hmap = new HashMap<String, String>();
        HashSet<String> hset = new HashSet<String>();
        hmap.put("A", "a");
        hmap.put("B", "b");
        hmap.put("C", "c");
        hset.add("A");
        hset.add("A");
        hset.add("A");

        System.out.println("...........HashMap..........");
        System.out.println("keys: " + hmap.keySet());
        System.out.println("values: " + hmap.values());
        System.out.println("key-value pairs: " + hmap.entrySet());
        for (String i : hmap.keySet()) {
            System.out.println("key: " + i + " value: " + hmap.get(i));
        }

        System.out.println("...........HashSet..........");
        System.out.println("HashSet: " + hset);
        System.out.println("HashSet size: " + hset.size());
    }
}
