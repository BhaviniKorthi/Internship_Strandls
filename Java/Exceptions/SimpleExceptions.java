

public class SimpleExceptions {

    public static void main(String[] args){
        System.out.println("Line1");
        try{
            System.out.println("Line11");
            System.out.println("Line12");
            System.out.println(10/0);
            System.out.println("Ending try block");

        }
        catch (ArithmeticException e){
            System.out.println("Exception occured..."+e);
        }
        finally{
            System.out.println("Finally block");
        }
        System.out.println("Line2");
    }
    
}
