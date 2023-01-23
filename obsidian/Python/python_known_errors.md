## [AttributeError: module 'httpcore' has no attribute 'SyncHTTPTransport](https://stackoverflow.com/questions/72796594/attributeerror-module-httpcore-has-no-attribute-synchttptransport)

```
googletrans==3.0.0 use very old httpx (0.13.3) and httpcore version. You just need to update httpx and httpcore to latest version and go to googletrans source directory in Python310/Lib/site-packages. In the file client.py, fix 'httpcore.SyncHTTPTransport' to 'httpcore.AsyncHTTPProxy'. And done, perfect. Even, Async, a concurrency model that is far more efficient than multi-threading, and can provide significant performance benefits and enable the use of long-lived network connections such as WebSockets. if you got error 'Nonetype'...group. Try: pip install googletrans==4.0.0-rc1

```


