#!/usr/bin/env python
import argparse
import json
import sys

def load_data_from_file (json_file):
  try:
    text = ""
    with open (json_file, "r") as f:
      return f.read ()
  except FileNotFoundError:
    sys.exit ("Le fichier indiqué n'existe pas.")

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

    


if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Joli reformattage de documents json.")
  parser.add_argument ('-f', '--file', type = str, \
      help = "Emplacement du fichier json à reformatter.", \
      dest = "file", required = False)
  parser.add_argument ('-i', '--stdin', action = 'store_true', \
      help = "On indente d'après la ligne de commande.", \
      dest = "from_stdin", default = True)
  args = parser.parse_args ()
  if args.file:
    save_to_file (args.file, reformat_json (load_data_from_file (args.file)))
    print ("Le fichier a été correctement réécrit.")
  elif args.from_stdin:
    print (reformat_json (sys.stdin.read ()))
