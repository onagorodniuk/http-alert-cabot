from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from django.db import models
from django.conf import settings
from django.template import Context, Template
from os import environ as env

import requests
import json

post_template = " {{ service }} Service {{ service.name }} {% if service.overall_status == service.PASSING_STATUS %}is back to normal{% else %}reporting {{ service.overall_status }} status{% endif %}: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %}. {% if service.overall_status != service.PASSING_STATUS %}Checks failing: {% for check in service.all_failing_checks %}{% if check.check_category == 'Jenkins check' %}{% if check.last_result.error %} {{ check.name }} ({{ check.last_result.error|safe }}) {{jenkins_api}}job/{{ check.name }}/{{ check.last_result.job_number }}/console{% else %} {{ check.name }} {{jenkins_api}}/job/{{ check.name }}/{{check.last_result.job_number}}/console {% endif %}{% else %} {{ check.name }} {% if check.last_result.error %} ({{ check.last_result.error|safe }}){% endif %}{% endif %}{% endfor %}{% endif %}"

class HttpAlert(AlertPlugin):

        name = "AlertHttp"
        author = "Oleksandr Nagorodniuk"

        def send_alert(self, service, users, duty_officers):

                c = Context({
                        'service': service,
                        'host': settings.WWW_HTTP_HOST,
                        'scheme': settings.WWW_SCHEME,
                        })

                message = Template(post_template).render(c)
                self.post_http(message, service=service)

        def post_http(self, message, service, color='green'):
                headers = {'content-type': 'text/plain'}
                data = str(message)
                url = 'http://someurl.com'
                resp = requests.post(url,data=data,headers=headers)

class HttpAlertUserData(AlertPluginUserData):
        name = "HttpAlert Plugin"
        key = models.CharField(max_length=32, blank=False, verbose_name="User/Group Key")
        alert_on_warn = models.BooleanField(default=True)
