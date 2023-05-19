class outer{
    int a = 100;
    class inner{
        int b = 200;
    }
}

public class practice {
    public static void main(String args[]){
        outer out = new outer();
        outer.inner in = out.new inner();
        System.out.println(out.a);  
        System.out.println(in.b);
        System.out.println(out.a + in.b);
    }
}
