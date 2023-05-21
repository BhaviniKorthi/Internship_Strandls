import java.io.*;
import java.io.IOException; 

public class FileHandling {
    public static void main(String[] args) {
        try{
            File f = new File("test.txt");
            boolean x = f.createNewFile();
            boolean y = f.delete();
            System.out.println(x + " " + y);
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

        try{
            FileWriter Write = new FileWriter("test1.txt");
            Write.write("Hello World");
            Write.close();
             
        }catch(IOException e){
            System.out.println("Exception occured..."+e);
        }
        File f2 = new File("test1.txt");
        System.out.println("Length of file is: "+f2.length()+" bytes");
       
    }
}
