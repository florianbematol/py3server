from py3server.app.service import Service


@Service()
class HealthService(object):

    def __init__(self):
        self.probes_name = ['api', 'frontend', 'market', 'messages']
        self.probes = dict([(x, True) for x in self.probes_name])

    def check_probe(self, probe):
        if probe != 'all':
            return self.probes[probe]
        else:
            return all(self.probes.values())

    def is_valid_probe(self, probe):
        return probe == 'all' or probe in self.probes_name
