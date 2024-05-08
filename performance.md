### Без кэша
Running 30s test @ http://192.168.1.70:8000/user/random/?limit=100
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   523.32ms  207.47ms   1.58s    86.64%
    Req/Sec    77.93     51.14   300.00     65.72%
  22810 requests in 30.06s, 5.81MB read
  Non-2xx or 3xx responses: 211
Requests/sec:    758.93
Transfer/sec:    198.02KB

### С кэшем
Running 30s test @ http://192.168.1.70:8000/user/random_cache/?limit=100
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   495.33ms   62.93ms 918.95ms   86.44%
    Req/Sec    68.73     42.53   300.00     73.85%
  23732 requests in 30.04s, 6.05MB read
  Socket errors: connect 0, read 207, write 0, timeout 0
  Non-2xx or 3xx responses: 207
Requests/sec:    790.01
Transfer/sec:    206.14KB