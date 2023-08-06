import json
from datetime import datetime
import urllib.request
import urllib.parse

api_base = "https://api.bugsnag.com/"
token = None

def set_token(t):
    global token
    token = t

def parse_date(date_str):
    curr = None
    try:
        curr = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000Z")
    except:
        pass
    if curr is None:
        print("Possibly invalid date format: %s" % date_str)
    return curr

class UnknownPropertyException(Exception):
    pass

class NoTokenException(Exception):
    pass

class Base():
    json = None

    def __init__(self, json):
        self.json = json

    def __getattr__(self, attr):
        if attr in self.json.keys(): 
            return self.json[attr]
        raise UnknownPropertyException("%s has no attribute '%s'" % (self.__class__.__name__, attr))

    @staticmethod
    def fetch(path, parser=None):
        if not token:
            raise NoTokenException('No token had been set!')
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('Authorization', "token %s" % token),
            ('X-Version', 2),
            ('Content-Type', 'application/json')
        ]
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(api_base + path).read()
        json_object = json.loads(response.decode('utf-8'))
        return json_object if parser is None else parser(json_object)

class Organization(Base):

    _projects = None

    def __getattr__(self, attr):
        if attr in ['projects']:
            if self._projects is None:
                self._projects = Project.fetch_all(self.id)
            return self._projects
        return super().__getattr__(attr)

    @staticmethod
    def fetch_all():
        return Organization.fetch('user/organizations', lambda oo: [Organization(o) for o in oo])

class Project(Base):

    _stability_trend = None

    def __getattr__(self, attr):
        if attr in ['stability_trend']:
            if self._stability_trend is None:
                self._stability_trend = StabilityTrend.fetch_stability_trend(self.id)
            return self._stability_trend
        return super().__getattr__(attr)


    @staticmethod
    def fetch_all(org_id):
        endpoint = "organizations/%s/projects?" % str(org_id)
        return Project.fetch(endpoint, lambda pp: [Project(p) for p in pp])

class StabilityTrend(Base):
    _timeline_points = None

    def __getattr__(self, attr):
        if attr in ['timeline_points']:
            if self._timeline_points is None:
                self._timeline_points = [TimelinePoint(t) for t in super().__getattr__(attr)]
            return self._timeline_points
        return super().__getattr__(attr)

    @staticmethod
    def fetch_stability_trend(project_id):
        endpoint = "projects/%s/stability_trend" % str(project_id)
        return StabilityTrend.fetch(endpoint, lambda data: StabilityTrend(data))

class TimelinePoint(Base):
    def __getattr__(self, attr):
        if attr in ['bucket_start', 'bucket_end']:
            return parse_date(super().__getattr__(attr))
        return super().__getattr__(attr)
