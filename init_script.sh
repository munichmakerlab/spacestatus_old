#!/bin/sh

# Quick start-stop-daemon example, derived from Debian /etc/init.d/ssh
set -e

# Must be a valid filename
NAME=mumalab_status
PIDFILE=/var/run/$NAME.pid
#This is the command to be run, give the full pathname
DAEMON=/var/www/vhosts/munichmakerlab.de/status/daemon.py
DAEMON_OPTS=""

export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"

case "$1" in
  start)
        echo -n "Starting daemon: "$NAME
	start-stop-daemon --start --quiet --background --make-pidfile --pidfile $PIDFILE --startas $DAEMON -- $DAEMON_OPTS
        echo "."
	;;
  stop)
        echo -n "Stopping daemon: "$NAME
	start-stop-daemon --stop --quiet --oknodo --remove-pidfile --pidfile $PIDFILE
        echo "."
	;;
  restart)
        echo -n "Restarting daemon: "$NAME
	start-stop-daemon --stop --quiet --oknodo --remove-pidfile --retry 30 --pidfile $PIDFILE
	start-stop-daemon --start --quiet --background --make-pidfile --pidfile $PIDFILE --startas $DAEMON -- $DAEMON_OPTS
	echo "."
	;;

  *)
	echo "Usage: "$1" {start|stop|restart}"
	exit 1
esac

exit 0
