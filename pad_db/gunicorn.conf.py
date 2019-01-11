bind = "192.168.1.200:8000"                   # Don't use port 80 becaue nginx occupied it already. 
errorlog = '/home/rohil/pad-db/logs/gunicorn-error.log'  # Make sure you have the log folder create
accesslog = '/home/rohil/pad-db/logs/gunicorn-access.log'
loglevel = 'debug'
workers = 3     # the number of recommended workers is '2 * number of CPUs + 1'
