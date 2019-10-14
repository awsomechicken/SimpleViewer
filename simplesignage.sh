#!/bin/sh
#
# /etc/init.d/mysystem
# Subsystem file for "MySystem" server
#
# chkconfig: 2345 95 05	(1)
# description: MySystem server daemon
#
# processname: MySystem
# config: /etc/MySystem/mySystem.conf
# config: /etc/sysconfig/mySystem
# pidfile: /var/run/MySystem.pid

# source function library
. /etc/rc.d/init.d/functions

# pull in sysconfig settings
[ -f /etc/sysconfig/mySystem ] && . /etc/sysconfig/mySystem	(2)

RETVAL=0
prog="MySystem"

start() {	(4)
	echo -n $"Starting $prog:"

	RETVAL=$?
	[ "$RETVAL" = 0 ] && touch /var/lock/subsys/$prog
	echo
}

stop() {	(6)
	echo -n $"Stopping $prog:"

	killproc $prog -TERM
	RETVAL=$?
	[ "$RETVAL" = 0 ] && rm -f /var/lock/subsys/$prog
	echo
}

reload() {	(8)
	echo -n $"Reloading $prog:"
	killproc $prog -HUP
	RETVAL=$?
	echo
}

case "$1" in	(9)
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		stop
		start
		;;
	reload)
		reload
		;;
	condrestart)
		if [ -f /var/lock/subsys/$prog ] ; then
			stop
			# avoid race
			sleep 3
			start
		fi
		;;
	status)
		status $prog
		RETVAL=$?
		;;
	*)	(10)
		echo $"Usage: $0 {start|stop|restart|reload|condrestart|status}"
		RETVAL=1
esac
exit $RETVAL
