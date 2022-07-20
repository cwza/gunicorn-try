## Different Type of Program
* CPU-Block program(ex: infinity loop), IO-Block program(ex: read file, HTTP, database connect)
* Concurrency on cpu-blocked: Multi-Processing, Multi-Threading
* Concurrency on io-blocked: Async (You can also combine this with Multi-Processing, Multi-Threading)

## Gunicorn Basic
* Master - Worker Architecture to achive multi processing
* One worker will fork one process
* Master(Arbiter) maintain the workers processes, It launches or kills them if needed
* There are some different type of worker: sync, gthread, gevent... worker
* gthread: easy to use multi-threading library, gevent: easy to use async library

## Worker Class
* sync: Multi-Processing
    + worker = 2, this means the max concurrency is 2
* gthread: Multi-Processing + Multi-Threading
    + worker = 2, thread = 2, this means the max concurrency is 4
* gevent: Multi-Processing + Async
    + worker = 2, this means the max io-blocking concurrency is infinity, but the max cpu-blocking concurrency is still 2

## Graceful Shutdown
* graceful_timeout: Timeout for graceful workers restart.
* when worker receive SIGTERM, it will set self.alive = False to not handle any request but only handle the current request untill graceful_timeout
* when master receive SIGTERM, it will send SIGTERM to all of the workers
* after the worker be killed, master will fork another worker to serve the new request

## Timeout
* timeout: Workers silent for more than this many seconds are killed and restarted.
* if the worker meet the timeout(maybe be blocked by some cpu-blocking code), the master will kill the worker directly by SIGABORT, so there is no graceful shutdown, the requests be serving by this worker will miss!!!
* if you set your timeout to be 30, the worker will modify a file each 15 sec, if master found that the file has not been modified a while, then it will kill the worker
* after the worker be killed, master will fork another worker to serve the new request

## Questions
* 當worker收到graceful-timeout通知以後, 還可以接客ㄇ
* 如果我ㄉworker是1, 然後當下的worker timeout了, 我是不是就不能收request了
    + 只要master還在都能收request, 只是沒worker可以處理時這個request會block在那邊等待worker來處理它
    + 詳情請洽tcp backlog
* 什麼時候會送timeout
    + 當你的worker被cpu block的request block超過timeout, 或者是你的app啟動時不管是cpu-block還是io-block超過timeout都會重啟
    + master在每次fork worker後run worker前都會重新把我們的app load進來, 所以如果你的app啟動時間大於timeout, worker就會在run之前被timeout
* 如果我timeout設定1他會喪心病狂ㄉ重啟ㄇ
    + 如果你的程式啟動超過1秒就會一直重啟, 如果你的程式一開始啟動小於1秒, 但某隻api cpu-block超過1秒, 這情況下就是你每次打那隻api就每次重啟
