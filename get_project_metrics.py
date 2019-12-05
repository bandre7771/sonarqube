import requests
import pdb
from requests.auth import HTTPDigestAuth

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

class SSLContextAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs['ssl_context'] = context
        context.load_default_certs() # this loads the OS defaults on Windows
        return super(SSLContextAdapter, self).init_poolmanager(*args, **kwargs)

url = 'https://sonar.aws.myhealth.va.gov/api/project_analyses/search?project=gov.va.med.mhv.admin:mhv-admin-common-dependencies'

s = requests.Session()
adapter = SSLContextAdapter()
s.auth = ("admin", "admin")
s.mount(url, adapter)
response = s.get(url)
print(str(response.content))