import java.io.File;
import java.io.IOException; 

public class FileHandling {
    public static void main(String[] args) {
        try{
            File f = new File("test.txt");
            boolean x = f.createNewFile();
            System.out.println("x:"+ x);
        }
        catch(IOException e){
            System.out.println("Exception occured..."+e);
        }
        try{
            File f1 = new File("test1.txt");
            boolean x = f1.createNewFile();
            System.out.println("new file");
        }
        catch(IOException e){
            System.out.println("Exception occured..."+e);
        }
       
    }
}
