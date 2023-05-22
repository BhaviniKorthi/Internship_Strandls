class even implements Runnable{
    public void run(){
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
    }
}

class odd implements Runnable{
    public void run(){
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
    }
}


public class UsingRunnable {
    public static void main(String[] args){
        even e = new even();
        odd o = new odd();
        Thread t1 = new Thread(e);
        Thread t2 = new Thread(o);
        t1.start();
        // try{
        //     Thread.sleep(100);
        // }catch(InterruptedException ex){
        //     System.out.println(ex);
        // }
        t2.start();
    }
}
