# Gunicorn
## Installation
```shell
$> pip install gunicorn
```
## Start
Command to test run the application using Gunicorn.  

```
$ gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app
```

`--workers N`

Set the --workers to two x the number of cores in your server. Adjust the number later if you have any issues. Do not exceed 12.

`--bind 0.0.0.0:5000`

This will listen on all server networking interfaces on port 5000.

`wsgi:app`

`wsgi` is the file name without the `.py` extension. `app` is the instance of the Flask application within the file. You should see the similar output below.

From [Deploy Flask The Easy Way With Gunicorn and Nginx!](https://dev.to/brandonwallace/deploy-flask-the-easy-way-with-gunicorn-and-nginx-jgc)
