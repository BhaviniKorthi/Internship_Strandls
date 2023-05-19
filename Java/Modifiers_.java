class Main {
    private int x;
    final int y = 200;

    public void setvalue(int val){
        this.x = val;
    }    

    public int getvalue(){
        return this.x;
    }
}


public class Modifiers_{

    public static void main(String[] args) {
        Main obj = new Main();
        obj.setvalue(100);

        System.out.println(obj.getvalue());

        Main obj2 = new Main();
        obj2.setvalue(200);

        System.out.println(obj2.getvalue());
        System.out.println(obj.getvalue());
    }

}