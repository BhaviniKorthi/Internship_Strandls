# REDIS CHEAT SHEET

## Key-value pairs 

- 127.0.0.1:6379> set mykey 100   #(mykey, "100") --> (key, value) 
  <br>OK

- 127.0.0.1:6379> get mykey  
 "100"

- 127.0.0.1:6379> set mykey1 "hello world"<br>
  OK
 
- 127.0.0.1:6379> get mykey1 <br>
  "hello world"

- 127.0.0.1:6379> keys *  #gives all the keys stored
1) "mykey1"
2) "mykey"


## Hash-map

- 127.0.0.1:6379> hmset hash A a B b C c D d  # hashmap with pairs [(A, a), (B, b), (C, c), (D, d)] 
  OK

- 127.0.0.1:6379> hgetall hash #get all pair in the hash
1) "A"
2) "a"
3) "B"
4) "b"
5) "C"
6) "c"
7) "D"
8) "d"

- 127.0.0.1:6379> hget hash A #get value for hashkey "A"
  "a"

- 127.0.0.1:6379> hmget hash A B #calling multiple hash keys
1) "a"
2) "b"

- 127.0.0.1:6379> hset hash E e #appending (E,e) pair to the present hash
  (integer) 1

- 127.0.0.1:6379> hgetall hash
 1) "A"
 2) "a"
 3) "B"
 4) "b"
 5) "C"
 6) "c"
 7) "D"
 8) "d"
 9) "E"
10) "e"

- 127.0.0.1:6379> hdel hash D E #delete the keys D and E
  (integer) 2

- 127.0.0.1:6379> hgetall hash 
1) "A"
2) "a"
3) "B"
4) "b"
5) "C"
6) "c"

## List

- 127.0.0.1:6379> lpush list a b c d e  #list is made with a, b, c, d, e elements
  (integer) 5

- 127.0.0.1:6379> lrange list 0 -1  #all the elements in the range
1) "e"
2) "d"
3) "c"
4) "b"
5) "a"

- 127.0.0.1:6379> lindex list 3 #element at index 3
  "b"

- 127.0.0.1:6379> lrange list 3 3
1) "b"

- 127.0.0.1:6379> linsert list before c new  #add a element before the element c--> linsert key before value newvalue
  (integer) 6

- 127.0.0.1:6379> lrange list 0 -1
1) "e"
2) "d"
3) "new"
4) "c"
5) "b"
6) "a"

- 127.0.0.1:6379> linsert list after c new  #add a element after the element c--> linsert key after value newvalue
  (integer) 7

- 127.0.0.1:6379> lrange list 0 -1
1) "e"
2) "d"
3) "new"
4) "c"
5) "new"
6) "b"
7) "a"

- 127.0.0.1:6379> llen list #length of list
  (integer) 7


## Sets

- 127.0.0.1:6379> sadd set a a b c d e c  #set 
  (integer) 5

- 127.0.0.1:6379> smembers set #elements in set
1) "a"
2) "d"
3) "b"
4) "c"
5) "e"

- 127.0.0.1:6379> srem set e  #remove element e
  (integer) 1

- 127.0.0.1:6379> smembers set
1) "d"
2) "b"
3) "c"
4) "a"

## Sorted sets

- 127.0.0.1:6379> zadd sortset 1 a 2 b 3 c 5 d 4 e 6 a 1 z  #sorted set in scores
  (integer) 6

- 127.0.0.1:6379> zrange sortset 0 -1 #all elements sorted according to scores
1) "z"
2) "b"
3) "c"
4) "e"
5) "d"
6) "a"

- 127.0.0.1:6379> zrange sortset 0 -1 withscores #sorted elements with their scores
 1) "z"
 2) "1"
 3) "b"
 4) "2"
 5) "c"
 6) "3"
 7) "e"
 8) "4"
 9) "d"
10) "5"
11) "a"
12) "6"

## Pub/Sub

- 127.0.0.1:6379> subscribe chat   #subscribed to a channel called "chat"
Reading messages... (press Ctrl-C to quit)  
1) "subscribe"
2) "chat"
3) (integer) 1

- 127.0.0.1:6379> publish chat "hello world" #publishing a message to channel "chat"
  (integer) 1

- 127.0.0.1:6379> subscribe chat  #the message got updated to the subsciber
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "chat"
3) (integer) 1
1) "message"
2) "chat"
3) "hello world"

