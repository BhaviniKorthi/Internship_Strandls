class ThreadRun implements Runnable {
    Thread t;
    String name;

    ThreadRun(String name) {
        this.name = name;
        t = new Thread(this, name);
        t.start();
    }

    public void run() {
        System.out.println("Thread " + this.name + " is running");
        for (int i = 0; i < 10; i++) {
            try{
                if (i==5 && this.name.equals("T-1")){
                    t.sleep(10000);
                    this.name = "Updated t-1";
                    t.setName(this.name);
                }
            }catch(InterruptedException e){
                System.out.println("Exception occured..."+e);
            }
            System.out.println("Thread " + this.name + " is running " + i);
        }
    }

}

public class Thread_ {
    public static void main(String[] args) {
        ThreadRun t1 = new ThreadRun("T-1");
        // t1.start();

        ThreadRun t2 = new ThreadRun("T-2");
        // t2.start();

    }
}
