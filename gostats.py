import urlparse

import requests

from util import headers
from checks import AgentCheck

class GoStats(AgentCheck):

    SERVICE_CHECK_NAME = 'gostats.is_ok'

    def check(self, instance):
        if 'gostats_url' not in instance:
            raise Exception("Missing 'gostats_url' in GoStats config")

        try:
            url = instance.get('gostats_url')
            parsed_url = urlparse.urlparse(url)
            gostats_host = parsed_url.hostname
            gostats_port = parsed_url.port or 8080

            r = requests.get(url, headers=headers(self.agentConfig))
            r.raise_for_status()
            status = r.json()
        
            for key, value in status.items():
                self.log.info('%s:%s' % (key, value))
                self.gauge('gostats.%s' % (key), value)
                
        except Exception, e:
            self.log.error('error: %s' % str(e))
            raise
