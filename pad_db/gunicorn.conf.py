bind = "192.168.1.200:8000"                   # Don't use port 80 becaue nginx occupied it already. 
errorlog = '/Users/rohil/Projects/pad-db/logs/gunicorn-error.log'  # Make sure you have the log folder create
accesslog = '/Users/rohil/Projects/pad-db/logs/gunicorn-access.log'
loglevel = 'debug'
workers = 1     # the number of recommended workers is '2 * number of CPUs + 1'
