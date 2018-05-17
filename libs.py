import json
import yaml
import sys
import re
import os.path
from random import randrange

def reformat_json (data):
  try:
    json_data = json.loads (data)
  except json.decoder.JSONDecodeError:
    sys.exit ("Les données fournies n'ont pas l'air d'être du json valide.")
  return json.dumps (json_data, sort_keys = True, indent = 2)

def save_to_file (json_file, data):
  try:
    with open (json_file, "w") as f:
      f.write (data)
  except FileNotFoundError:
    sys.exit ("Le fichier indiqué ({}) n'existe pas.".format (json_file))

def load_data_from_file (json_file):
  try:
    text = ""
    with open (json_file, "r") as f:
      return f.read ()
  except FileNotFoundError:
    sys.exit ("Le fichier indiqué ({}) n'existe pas.".format (json_file))

def json2yaml (data):
  try:
    return yaml.dump(json.loads(data), default_flow_style=False)
  except Exception as e:
    sys.exit ("Erreur dans json2yaml : {}".format (e))

def extract_attributes_from_php_code (php_code):
  regexp = re.compile ('^\s*(protected|private|public)\s+\$(?P<var_name>.+)\s*[=;].*$')
  result = []
  for line in php_code.split ("\n"):
    m = re.match (regexp, line.strip ())
    if m:
      result.append (m.group ('var_name'))
  return result

def map_from_type_to_mock (input_type):
  classic_input_type = input_type.lower ()
  types = {
    'integer': 'integer',
    'string': 'string',
    'text': 'string',
    'datetime': 'datetime',
    'boolean': 'bool',
    'decimal': 'decimal',
    'float': 'decimal',
  }
  if classic_input_type in types:
    return types[classic_input_type]
  return 'file'

def extract_data_from_php_file (php_file):
  attribute_name_regexp = re.compile ('^\s*(protected|private|public)\s+\$(?P<var_name>.+)\s*[=;].*$')
  attribute_type_regexp = re.compile ('^\s*\*.+((Column.*type)|(ManyToMany.+targetEntity)|(OneToOne.+targetEntity))\s*=\s*"(?P<type>[^"]+)".*$')
  result = {
    'classname': extract_classname_from_php_file (php_file),
    'attributes': {}
  }
  last_seen = [ None, None ]
  for line in load_data_from_file (php_file).split ('\n'):
    line = line.strip ()
    attribute_name = re.match (attribute_name_regexp, line)
    attribute_type = re.match (attribute_type_regexp, line)

    if last_seen and attribute_name:
      result['attributes'][attribute_name.group ('var_name')] = last_seen
      last_seen = [ None, None ]
    elif attribute_type:
      last_seen = [ map_from_type_to_mock (attribute_type.group ('type')), None ]
      if last_seen[0] == "file":
        last_seen[1] = php_file.replace (result['classname'], attribute_type.group ('type'))
  return (result)


def extract_classname_from_php_file (php_file):
  regexp = re.compile ('^\s*class\s+(?P<class_name>.+)\s*$')
  for line in load_data_from_file (php_file).split ('\n'):
    m = re.match (regexp, line.strip ())
    if m:
      return m.group ('class_name')
  return None

def make_random_data_from_attributes (attributes, randomizer_token = None):
  inject_values = {
    "string": "chaine aléatoire",
    "integer": randrange (0, 100),
    "datetime": "01-01-1970T00:00:00Z",
    "bool": randrange (0, 1),
    "decimal": float ("{}.{}".format (randrange (5), randrange (100)))
  }
  if randomizer_token:
    inject_values['string'] += " "+randomizer_token
  result = {}
  for a in attributes:
    print ("Traitement de la clef {} ({})".format (a, attributes[a]))
    if (a != 'id'):
      if attributes[a][0] != "file":
        result[a] = inject_values[attributes[a][0]]
      else:
        print ("On va chercher dans {}".format (attributes[a][1]))
        result[a] = make_random_data_from_attributes (extract_data_from_php_file (attributes[a][1])['attributes'], randomizer_token)
  return result
