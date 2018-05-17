import json
import yaml
import sys
import re
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
    sys.exit ("Le fichier indiqué n'existe pas.")

def load_data_from_file (json_file):
  try:
    text = ""
    with open (json_file, "r") as f:
      return f.read ()
  except FileNotFoundError:
    sys.exit ("Le fichier indiqué n'existe pas.")

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
  input_type = input_type.lower ()
  types = {
    'integer': 'integer',
    'string': 'string',
    'text': 'string',
    'datetime': 'datetime'
  }
  if input_type in types:
    return types[input_type]
  return string

def extract_typed_attributes_from_php_code (php_code):
  attribute_name_regexp = re.compile ('^\s*(protected|private|public)\s+\$(?P<var_name>.+)\s*[=;].*$')
  attribute_type_regexp = re.compile ('^\s*\*.+Column.*type\s*=\s*"(?P<type>[^"]+)".*$')
  result = {}
  last_seen_type = None
  for line in php_code.split ('\n'):
    line = line.strip ()
    attribute_name = re.match (attribute_name_regexp, line)
    attribute_type = re.match (attribute_type_regexp, line)

    if last_seen_type and attribute_name:
      result[attribute_name.group ('var_name')] = last_seen_type
      last_seen_type = None
    elif attribute_type:
      last_seen_type = map_from_type_to_mock (attribute_type.group ('type'))

  return (result)


def extract_classname_from_php_code (php_code):
  regexp = re.compile ('^\s*class\s+(?P<class_name>.+)\s*$')
  for line in php_code.split ("\n"):
    m = re.match (regexp, line.strip ())
    if m:
      return m.group ('class_name')
  return None

def make_random_data_from_attributes (attributes, randomizer_token = None):
  inject_values = {
    "string": "chaine aléatoire",
    "integer": randrange (0, 100),
    "datetime": "01-01-1970T00:00:00Z"
  }
  if randomizer_token:
    inject_values['string'] += " "+randomizer_token
  result = {}
  for a in attributes:
    if (a != 'id'):
      result[a] = inject_values[attributes[a]]
  return result
