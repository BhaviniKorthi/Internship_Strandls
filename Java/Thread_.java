public class Thread_ implements Runnable {

    public void run(){
        System.out.println("Thread is running");
    }
    public static void main(String[] args) {
        Runnable t1 = new Thread_();
        // Runnable t2 = new Thread_();

        Thread t2 = new Thread(t1, "Create new thread");

        // t1.start();
        // t2.start();
        System.out.println(t2.getName());
        t2.start();
    }
    
}
