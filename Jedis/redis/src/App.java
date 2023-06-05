import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPooled;

public class App {
    public static void main(String[] args) {
        // Create a Jedis client
        JedisPooled jedis = new JedisPooled("localhost", 6379);

        
        // Use Redis commands through the Jedis instance
        // ...
        
        // Remember to close the connection
        jedis.close();
    }
}
