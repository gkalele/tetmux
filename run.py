#!/usr/bin/env python

import jinja2
import os
import sys

CLUSTER = os.getenv("CLUSTER")
VCLUSTER = os.getenv("VCLUSTER")
CLS = ""
ARTIFACTS="artifacts"

def validate_args():
    if CLUSTER and VCLUSTER:
        sys.exit("Cannot specify both CLUSTER and VCLUSTER environment variables")
    if not (CLUSTER or VCLUSTER):
        sys.exit("Must specify either CLUSTER or VCLUSTER environment variables")

def render(template_file, d):
    path, filename = os.path.split(template_file)
    jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(path or './'))
    return jenv.get_template(filename).render(d)
        
def render_templates():
    global CLS
    print "Rendering templates for %s/%s" % (CLUSTER, VCLUSTER)
    if CLUSTER:
        CLS=CLUSTER
        BARE=CLUSTER
    else:
        CLS="vcluster%s" % VCLUSTER
        BARE=VCLUSTER
    d = {"CLS":CLS, "BARE": BARE}
    runContents = render("run.j2", d)
    with open("%s/run%s.sh"%(ARTIFACTS,CLS), "wt") as fd:
        fd.write(runContents)
    ymlContents = render("cluster.yml.j2", d)
    with open("%s/%s.yml"%(ARTIFACTS,CLS), "wt") as fd:
        fd.write(ymlContents)
    print "Generated tmux runfile and yml file for %s" % CLS
    os.system("cd ARTIFACTS; bash run%s.sh" % CLS)

def connect():
    print "Connecting to %s" % CLS
    
if __name__ == "__main__":
    validate_args()
    render_templates()
    if sys.argv[1] == "connect":
        connect()
