/*public class ThreadUsingLambda {

    public static void main(String[] args){

        Runnable  r1 = () -> {
            for(int i=0;i<=10;i++){
                if(i%2==0){
                    System.out.println("Even number: "+i);
                    try{
                        Thread.sleep(100);
                    }
                    catch(InterruptedException e){
                        System.out.println(e);
                    }
                }
            }
        };

        Runnable  r2 = () -> {
            for(int i=0;i<=10;i++){
                if(i%2!=0){
                    System.out.println("Odd number: "+i);
                    try{
                        Thread.sleep(100);
                    }
                    catch(InterruptedException e){
                        System.out.println(e);
                    }
                }
            }
        };


        Thread t1 = new Thread(r1);
        Thread t2 = new Thread(r2);
        t1.start();
        t2.start();

    }
    
}*/

public class ThreadUsingLambda {
    public static void main(String[] args) throws Exception {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i <= 10; i++) {
                if (i % 2 == 0) {
                    System.out.println("Even number: " + i);
                }
            }
        },"Even Thread");

        Thread t2 = new Thread(() -> {
            for (int i = 0; i <= 10; i++) {
                if (i % 2 != 0) {
                    System.out.println("Odd number: " + i);
                }
            }
        },"Odd Thread");

        // t1.setName("Even Thread");
        // t2.setName("Odd Thread");
        System.out.println(t1.getName());
        System.out.println(t2.getName());
        //Priority
        t1.setPriority(2);
        t2.setPriority(3);
        System.out.println(t1.getPriority());
        System.out.println(t2.getPriority());

        t1.start();
        t2.start();
        System.out.println(t1.isAlive());
        t1.join();
        System.out.println(t1.isAlive());
    
        // t2.join();
        System.out.println("End of the code");
    }
}
