class Even extends Thread{
    public void run(){
        for(int i=0;i<10;i+=2){
            System.out.println(i);
            try{
                Thread.sleep(1000);
            }catch (InterruptedException e){System.out.println(e);}
            
        }
    }
}

class Odd extends Thread{
    public void run(){
        for(int i=1;i<10;i+=2){
            System.out.println(i);
            try{
                Thread.sleep(1000);
            }catch (InterruptedException e){System.out.println(e);}
        }
    }
}

public class UsingThread {

    public static void main(String[] args){
        Even e = new Even();
        Odd o = new Odd();
        e.start();
        o.start();
    }
    
} 

