import os
import re
import yaml

def files():
  return os.listdir("./articles")

def metadata(filename):
  f = open("./articles/"+filename)
  contents = f.read()
  match = re.search('---\n(.+?)\n---', contents, flags=re.DOTALL)
  yaml_block = match.group(1)
  return yaml.load(yaml_block)

def run():
  if re.search("MegaPhysics$", os.getcwd()) == None:
    raise Exception("This script must be run from the root MegaPhysics directory")
  os.system("rm -r build")
  os.system("mkdir build")
  for f in files():
    print "rendering "+f
    data = metadata(f)
    course = data.get('course')
    if course == None:
      raise Exception(f+ " metadata has no 'course' entry")
    os.system("mkdir build/"+course)
    os.system("pandoc -s -t html5 --template=template.html -o build/"+course+"/"+f.replace(".md", ".html")+" articles/"+f)

run()