import json
import yaml
import sys
import re

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

def extract_classname_from_php_code (php_code):
  regexp = re.compile ('^\s*class\s+(?P<class_name>.+)\s*$')
  for line in php_code.split ("\n"):
    m = re.match (regexp, line.strip ())
    if m:
      return m.group ('class_name')
  return None

def make_random_data_from_attributes (attributes, randomizer_token = None):
  inject_value = "chaine aléatoire"
  if randomizer_token:
    inject_value += " "+randomizer_token
  result = {}
  for a in attributes:
    if (a != 'id'):
      result[a] = inject_value
  return result
