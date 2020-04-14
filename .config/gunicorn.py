daemon = False

chdir = '/srv/Netflex_Clone_Backend/app'
bind = 'unix:/run/netflex.sock'
accesslog = '/var/log/gunicorn/netflex-access.log'
errorlog = '/var/log/gunicorn/netflex-error.log'
capture_output = True
