import requests
import pdb
import json
from requests.auth import HTTPDigestAuth

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

class SSLContextAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs['ssl_context'] = context
        context.load_default_certs() # this loads the OS defaults on Windows
        return super(SSLContextAdapter, self).init_poolmanager(*args, **kwargs)

def get_project_names(projects_response):
	pkeys = []
	projects = projects_response.split("components")[1]
	projects = projects.split("organization")
	for project in projects:
		tokens = project.split(",")
		for token in tokens:
			if "key" in token:
				project_name = token.strip("\"key\":")
				pkeys.append(project_name)

	return pkeys


def get_project_stats(coverage):
	print(coverage["component"]["name"])
	measures = coverage["component"]["measures"]
	for measure in measures:
		print(str(measure["metric"]) + "=" + str(measure["value"]))
	print("\n")

def get_projects_stats(session, adapter, pkeys):
	for project_key in pkeys:
		url = "https://sonar.aws.myhealth.va.gov/api/measures/component?metricKeys=coverage,ncloc,lines_to_cover,complexity,violations,code_smells&component="+project_key
		session.mount(url, adapter)
		project_data = json.loads(session.get(url).content)
		if "component" in str(project_data):
			get_project_stats(project_data)

def main():
	url = 'https://sonar.aws.myhealth.va.gov/api/projects/search'
	session = requests.Session()
	adapter = SSLContextAdapter()
	session.auth = ("vhaslcandreb", "ba_sonar")
	session.mount(url, adapter)

	response = session.get(url)
	pkeys = get_project_names(str(response.content))
	project_stats = get_projects_stats(session, adapter, pkeys)

main()