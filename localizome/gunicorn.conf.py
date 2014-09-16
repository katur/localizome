import multiprocessing
bind = "unix:/tmp/gunicorn.sock"
max_requests = 1000
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 30
