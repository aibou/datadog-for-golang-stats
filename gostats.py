import urlparse

import requests

from util import headers
from checks import AgentCheck

class GoStats(AgentCheck):
    GAUGES = [
        'cpu_num',
        'cgo_call_num',
        'goroutine_num',
        'gomaxprocs',
        'memory_alloc',
        'memory_total_alloc',
        'memory_lookups',
        'memory_mallocs',
        'memory_sys',
        'memory_frees',
        'memory_stack',
        'heap_alloc',
        'heap_sys',
        'heap_idle',
        'heap_inuse',
        'heap_released',
        'heap_objects',
        'gc_num',
        'gc_per_second',
        'gc_pause_per_second',
    ]

    HISTGRAMS = [
        'gc_pause'
    ]

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

            for metric in self.GAUGES:
                if status.get(metric) is None:
                    continue
                self.gauge('gostats.%s' % (metric), status.get(metric))

            for metric in self.HISTGRAMS:
                if status.get(metric) is None:
                    continue
                for value in status.get(metric):
                    self.histogram('gostats.%s' % (metric), value)

        except Exception, e:
            self.log.error('error: %s' % str(e))
            raise
