import java.time.*;
import java.time.format.DateTimeFormatter;


public class DatePractice {

    public static void main(String[] args){
        LocalDate date = LocalDate.now();
        LocalTime time = LocalTime.now();
        LocalDateTime dateTime = LocalDateTime.now();
        System.out.println(date);
        System.out.println(time);
        System.out.println(date.plusDays(2));
        System.out.println(dateTime);
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MMM-dd-yyyy HH:mm:ss");
        System.out.println("Formatted:"+ formatter.format(dateTime));

    }

    
    
}
