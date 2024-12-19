import multiprocessing

workers = 8 #multiprocessing.cpu_count() * 2 + 1


access_logfile = '/var/log/gunicorn_access.log'
error_logfile = '/var/log/gunicorn_error.log'
log_level = 'debug'
capture_output = True
timeout=8000
