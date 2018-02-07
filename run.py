#!/usr/bin/env python

import jinja2
import os
import sys

cluster = os.getenv("CLUSTER")
ARTIFACTS="artifacts"

def validate_args():
    if not cluster:
        sys.exit("Must specify the CLUSTER environment variable")

def render(template_file, d):
    path, filename = os.path.split(template_file)
    jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(path or './'))
    return jenv.get_template(filename).render(d)
        
def render_templates():
    global cluster
    print "Rendering templates for " + cluster
    d = {"CLS":cluster}
    runContents = render("run.j2", d)
    with open("%s/run%s.sh"%(ARTIFACTS,cluster), "wt") as fd:
        fd.write(runContents)
    ymlContents = render("cluster.yml.j2", d)
    with open("%s/%s.yml"%(ARTIFACTS,cluster), "wt") as fd:
        fd.write(ymlContents)
    print "Generated tmux runfile and yml file for %s" % cluster
    os.system("cd ARTIFACTS; bash run%s.sh" % cluster)

def connect():
    print "Connecting to %s" % cluster
    
if __name__ == "__main__":
    validate_args()
    render_templates()
    if sys.argv[1] == "connect":
        connect()
