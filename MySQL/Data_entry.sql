
use bhavini_sample;
drop procedure populate_sample;
delimiter //
CREATE PROCEDURE populate_sample()
BEGIN
    DECLARE name varchar(20);
    DECLARE gender varchar(10);
    DECLARE phone numeric(10);
    DEClARE roll_number numeric(8) DEFAULT 10000000;
    DECLARE email_id varchar(100);
    DECLARE counter INT DEFAULT 1;
    WHILE (counter <= 10) DO -- change 10 to the desired number of tuples to insertw
        SET roll_number = roll_number + 1 ; 
        SET name = concat("Student",roll_number);
        SET gender = elt(FLOOR(1 + rand()*3 ), "Female", "Male", "Others") ; 
        SET phone = roll_number*100 + counter;
        SET email_id = concat( roll_number,  "@iitgn.ac.in");
        INSERT INTO Sample(name, gender, phone, roll_number, email_id)
        VALUES (name, gender, phone, roll_number, email_id);

        

        SET counter = counter + 1;
    END WHILE ;

END //
delimiter ;

call populate_sample();