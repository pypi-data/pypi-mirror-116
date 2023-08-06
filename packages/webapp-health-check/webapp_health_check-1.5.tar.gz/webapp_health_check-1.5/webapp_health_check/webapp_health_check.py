#
# documentation:
import requests
import json
import urllib3

# Return codes expected by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

#Disable warnings https
urllib3.disable_warnings()

class WebAppHealthChecks:
    def __init__(self, url, app_name):
        
        #initial
        self.url = url
        self.app_name = app_name
               

    def get_status_data(self):
            
        #Add tags to the URL
        url = self.url
        app_name = self.app_name
       
        # requests doc http://docs.python-requests.org/en/v0.10.7/user/quickstart/#custom-headers
        r = requests.get(url=url, verify=False)
        
        return r.json(), r.status_code
    
    def check_status_data(self):

        #Vars
        retrcode = OK
		#Create tuple with json and status code
        webapp_health_status = self.get_status_data()       

        msgdata = ''
        msgerror = '{:>10}'.format(webapp_health_status[0].get('entries').get(self.app_name).get('description', ''))           
        retrperfdata = ''
        retrmsg = ''
        
        #Validate Data
        if webapp_health_status[0]['status'] != 'Healthy':
            retrcode = CRITICAL

        msgerror += msgdata
         
        return retrcode, msgerror
        