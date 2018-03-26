#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import argparse
try:
  from yaml import load, YAMLError
except ModuleNotFoundError:
  import sys
  sys.exit ("Le module PyYAML ne semble pas présent sur votre système.")

CONST = {}
CONST['FILE_NOT_FOUND'] = "Le fichier demandé n'est pas accessible."
CONST['INVALID_FILE'] = "Le fichier est invalide."

def get_label (tag):
  try:
    return CONST[tag]
  except KeyError:
    return tag

def validate_yaml_file (file_name):
  result = {
    'result': False,
    'tag': '',
    'comments': []
  }
  try:
    with open (file_name, 'r') as f:
      try:
        load (f)
        result ['result'] = True
      except YAMLError as e:
        result ['result'] = False
        result ['tag'] = 'INVALID_FILE'
        if hasattr(e, 'problem_mark'):
          mark = e.problem_mark
          result ['comments'].append ('{}:{}'.format (mark.line+1, mark.column+1))
  except FileNotFoundError as e:
    result ['result'] = False
    result ['tag'] = 'FILE_NOT_FOUND'
  return result


if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Validation d'un fichier au format YAML." )
  parser.add_argument ('--file', type = str, \
      help = "Emplacement du fichier à valider.", \
      dest = "file", required = True)
  args = parser.parse_args ()
  result = validate_yaml_file (args.file)
  if result['result']:
    print ("Le fichier {} semble valide.".format (args.file))
  else:
    print ("Le fichier {} semble invalide : ".format (args.file))
    print (" * {}".format (get_label (result['tag'])))
    print (" * Commentaires du parser : ")
    print ("  * {}".format ("\n  * ".join (result['comments'])))
