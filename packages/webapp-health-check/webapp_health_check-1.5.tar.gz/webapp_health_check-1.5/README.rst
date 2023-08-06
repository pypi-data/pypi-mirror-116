Description
===========

Checks web apps health.

`VERSION  <webapp_health_check/VERSION>`__

Install
=======

Linux::

    sudo pip3 install webapp_health_check --upgrade

Also is possible to use::

    sudo python3 -m pip install webapp_health_check --upgrade

On windows with python3.5::

    pip install webapp_health_check --upgrade

For proxies add::

    --proxy='http://user:passw@server:port'

Usage
=====

Use the command line::

    > webapp_health_check --help
      usage: webapp_health_check [-h] [-u [URL]] [-a [APP_NAME]] [-e [EXTRA_ARGS]]

        optional arguments:
        -h, --help            show this help message and exit
        -u [URL], --url [URL]
                              url to check 		
        -a [APP_NAME], --app_name [APP_NAME]
                              app_name is the key entry where the description is located
        -e [EXTRA_ARGS], --extra_args [EXTRA_ARGS]
                              extra args


Example usage
=============

Example use:

    > webapp_health_check -u "https://xxx/" -a process_app_name

    {"status":"Healthy","totalDuration":"00:00:02.4136092","entries":{"process_app_name":{"data":{},"description":"Process health check was successful.","duration":"00:00:02.4106469","status":"Healthy"}}}     

Nagios config
=============

Example command::

    define command{
        command_name  webapp_health_check
        command_line  /usr/local/bin/webapp_health_check -u "$ARG1$" -a "$ARG2$" --extra_args='$ARG3$'
    }

Example service::

    define service {
            host_name                       SERVERX
            service_description             service_name
            check_command                   webapp_health_check!http://url/!process_app_name
            use				                generic-service
            notes                           some useful notes
    }

You can use ansible role that already has the installation and command: https://github.com/CoffeeITWorks/ansible_nagios4_server_plugins


