import json
import yaml
import sys

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
