#!/usr/bin/env python

import datetime
import json
import requests
import sys
from optparse import OptionParser

class ChkRundeck:
    def get_job_cnt(self, host, port, token, project, type, msec):
        url = "http://" + host + ":" + port + "/api/14/project/" + project + "/history"
        params = {
            "authtoken": token,
            "statFilter": type,
            "format": "json",
            "begin": msec
        }
        r = requests.post(url, params=params)
        job_cnt = r.json()["paging"]["total"]
        return job_cnt


    def get_job_list(self, host, port, token, project):
        url = "http://" + host + ":" + port + "/api/14/project/" + project + "/jobs"
        params = {
            "authtoken": token,
            "format": "json"
        }
        r = requests.post(url, params=params)
        return r.json()


    def get_system_info(self, host, port, token):
        url = "http://" + host + ":" + port + "/api/14/system/info"
        params = {
            "authtoken": token,
            "format": "json"
        }
        r = requests.post(url, params=params)
        return r.json()

    def get_running_executions(self, host, port, token, project):
        url = "http://" + host + ":" + port + "/api/14/project/" + project + "/executions/running"
        params = {
            "authtoken": token,
            "format": "json"
        }
        r = requests.post(url, params=params)
        return r.json()


    def main(self):
        parser = OptionParser(usage="usage: %prog [-h] [-p PORT] [-t API_TOKEN ] [-P PROJECT] [-T TYPE] [-m MIN] [HOSTNAME|IPADDR]")
        parser.set_defaults(port = "4440")
        parser.add_option("-p", "--port", dest="port", metavar="PORT",
                          help="default rundeck Web port [default: 4440]")
        parser.set_defaults(token = "")
        parser.add_option("-t", "--token", dest="token", metavar="TOKEN",
                          help="rundeck API token [default: '']")
        parser.set_defaults(project = "")
        parser.add_option("-P", "--project", dest="project", metavar="PROJECT",
                          help="rundeck project name [default: '']")
        parser.set_defaults(type = "")
        parser.add_option("-T", "--type", dest="type", metavar="TYPE",
                          help="the type of information to get [default: '']")
        parser.set_defaults(min = 5)
        parser.add_option("-m", "--min", dest="min", metavar="MIN",
                          help="get data from N minutes before [default: 5]")
        (options, args) = parser.parse_args()

        if (args):
            host=args[0]
        else:
            parser.error("HOSTNAME is required.")
            sys.exit(1)

        now = datetime.datetime.now()
        delta = datetime.timedelta(minutes=int(options.min))
        five_min_ago = now - delta
        utime_msec = int(five_min_ago.strftime('%s')) * 1000 + five_min_ago.microsecond / 1000

        if options.type == "succeed" or options.type == "fail" :
            job_cnt = self.get_job_cnt(host, options.port, options.token, options.project, options.type, utime_msec) 
        elif options.type == "running":
            running_jobs = self.get_running_executions(host, options.port, options.token, options.project)
            job_cnt = running_jobs["paging"]["total"]
        elif options.type == "listed":
            job_list = self.get_job_list(host, options.port, options.token, options.project) 
            job_cnt = len(job_list)
        else:
            print "you must set type."
            sys.exit(3)

        print(job_cnt)
        sys.exit()


if __name__ == "__main__":
  ChkRundeck().main()

