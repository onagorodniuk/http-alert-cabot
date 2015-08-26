Forked from https://github.com/colymore/http-alert-cabot with simple changes which are realise different POST "style"
When we have failed check we are POSTing such POST data:

Service %Your service name% reporting WARNING status: http://cabot.sample.com/service/2/. Checks failing:  %your check name%  (Hosts missing | 0/1 hosts)

Instalation

pip install git+git://github.com/onagorodniuk/cabot_alert_telegram.git

Also you need to change your env config, add:

vi 'cabot install dir'/conf/production.env
CABOT_PLUGINS_ENABLED=cabot-http-alert-plugin==0.1

