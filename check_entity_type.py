#!/usr/bin/env python
import argparse
import sys
import re
from libs import load_data_from_file#, save_to_file, extract_attributes_from_php_code

def extract_attributes_and_functions_and_phpdoc_from_phpcode(php_code):
  doctrine_annotation = re.compile('^\s*\*.*@ORM.Column\s*\((?P<column_parameters>.+)\).*$')
  php_attribute = re.compile ('^\s*(protected|private|public)\s+\$(?P<var_name>.+)\s*[=;].*$')
  phpdoc_var_type = re.compile('^\s*\*.*@var\s+(?P<var_type>.+)\s*$')
  phpdoc_param = re.compile('^\s*\*.*@param\s*(?P<var_type>.+)\s+(?P<var_name>\$.*)$')
  phpdoc_return = re.compile('^\s*\*.*@return\s*(?P<var_type>.+)$')
  php_getter = re.compile('^\s*public function (?P<getter>get.*)\(\)\s*(?P<return_type>.*)$')
  php_setter = re.compile('^\s*public function (?P<setter>set.*)\((?P<param_type>.*)\$.*\)\s*$')
  php_setter = re.compile('^\s*public function (?P<setter>set.*)\((?P<param_type>.*)\$.*$')

  attributes = {}
  functions = {}
  temp_annotation = {}
  temp_phpdoc = ""
  temp_phpdoc_param = {}
  temp_phpdoc_return = ""
  for line in php_code.split ("\n"):
    line = line.strip()
    """
    Dans cette section on va essayer de chopper les attributs PHP avec les types doctrine associés.
    """
    m1 = re.match(doctrine_annotation, line)
    if m1:
      """
      m.group('column_parameters') = type="datetime", nullable=false
      """
      for truc in m1.group('column_parameters').split(','):
        (key, value) = re.sub("""["']""", '', truc.strip()).split('=')
        temp_annotation[key] = value
    else:
      """Pas sûr qu'il soit obligatoire celui là, je le garde en facultatif."""
      m2 = re.match(phpdoc_var_type, line)
      if m2:
        temp_phpdoc = m2.group('var_type')
      else:
        m3 = re.match(php_attribute, line)
        if m3 and len(temp_annotation):
          attributes[m3.group('var_name')] = {
            'doctrine': temp_annotation,
            'phpdoc': temp_phpdoc
          }
          temp_annotation = {}
          temp_phpdoc = ""
    """
    On repart à 0 pour essayer de chopper les fonctions Xetters.
    Ce qui intéresse ici : 
    * @param
    * @return
    * le type de retour des getters,
    * le type d'entrée des setters
    """

    f1 = re.match(phpdoc_param, line)
    if f1:
      temp_phpdoc_param[f1.group('var_name')] = f1.group('var_type')
    else:
      f2 = re.match(phpdoc_return, line)
      if f2:
        temp_phpdoc_return = f2.group('var_type')
      else:
        f3 = re.match(php_getter, line)
        if f3 and temp_phpdoc_return:
          functions[f3.group('getter')] = {
            'phpdoc': temp_phpdoc_return,
            'php': f3.group('return_type')
          }
          temp_phpdoc_return = ""
        else:
          f4 = re.match(php_setter, line)
          if f4 and len(temp_phpdoc_param):
            functions[f4.group('setter')] = {
              'phpdoc': temp_phpdoc_param,
              'php': f4.group('param_type')
            }
            temp_phpdoc_param = {}
  return {
    'attributes': attributes,
    'functions': functions
  }

def compare_types(doctrine_type, phpdoc_type):
  result = False
  mapping = [
    [ 'integer', 'int' ],
    [ 'text', 'string' ],
    [ 'string', 'string' ],
    [ 'boolean', 'bool' ],
    [ 'datetime', '\\DateTime' ],
  ]
  if doctrine_type == phpdoc_type:
    result = True

  for m in mapping:
    if m[0] == doctrine_type and m[1] == phpdoc_type:
      result = True

  return result

def is_attribute_nullable_in_doctrine_and_phpdoc(doctrine_params, phpdoc_type):
  result = False

  if 'nullable' in doctrine_params:
    if doctrine_params['nullable'].lower() == 'false':
      """Non nullable dans doctrine donc ne doit pas démarrer par un ? dans la phpdoc."""
      if phpdoc_type[:1] != "?":
        result = True
    elif doctrine_params['nullable'].lower() == 'true':
      """Nullable dans doctrine donc doit démarrer par un ? dans la phpdoc."""
      if phpdoc_type[:1] == "?":
        result = True
    else:
      raise Exception('{} inconnu pour valeur de nullable.'.format(doctrine_params['nullable']))
  else:
    """Je fais l'hypothèse que par défaut doctrine fout les champs nullables."""
    if phpdoc_type[:1] == "?":
      result = True

  return result

def is_attribute_same_in_phpcode_and_phpdoc(phpcode, phpdoc):
  result = False
  phpcode = phpcode.strip()
  phpdoc = phpdoc.strip()
  """
  phpcode = int & phpdoc = int => True
  phpcode = ?int & phpdoc = int|null => True
  sinon => False
  """
  if phpcode == phpdoc:
    result = True
  else:
    phpdoc = re.sub("^(.+)\|null$", '?\g<1>', phpdoc)
    if phpcode == phpdoc:
      result = True

  return result

def validate_attributes(attributes):
  """
  On va essayer de faire un contrôle des attributs : 
  si nullable dans doctrine, alors la phpdoc doit être préfixée d'un `?`.
  """
  for attr in attributes:
    print ("Attribut : {}".format (attr))
    if compare_types(attributes[attr]['doctrine']['type'], attributes[attr]['phpdoc']):
      print ("  [OK] Cohérent sur le type déclaré dans la phpdoc et dans le code php.")
    else:
      print ("  [KO] Incohérent sur le type déclaré dans la phpdoc et dans le code php.")

    if is_attribute_nullable_in_doctrine_and_phpdoc(attributes[attr]['doctrine'], attributes[attr]['phpdoc']):
      print ("  [OK] Cohérent sur nullable dans doctrine et dans la phpdoc")
    else:
      print ("  [KO] Incohérent sur nullable dans doctrine et dans la phpdoc")

def validate_getter(function):
  function['php'] = re.sub('^\s*:\s*', '', function['php'])
  if is_attribute_same_in_phpcode_and_phpdoc(function['php'], function['phpdoc']):
    print('  [OK] Type de retour cohérent.')
  else:
    print('  [KO] Type de retour incohérent ({} !~ {}).'.format(function['php'], function['phpdoc']))

def validate_setter(function):
  """{'phpdoc': {'$debutPeriodeLitige': '\\DateTime'}, 'php': '?\\DateTime '}"""
  phpdoc_type = function['phpdoc'][list(function['phpdoc'].keys())[0]].strip()
  function['php'] = function['php'].strip()

  if is_attribute_same_in_phpcode_and_phpdoc(function['php'], phpdoc_type):
    print('  [OK] Type de retour cohérent.')
  else:
    print('  [KO] Type de retour incohérent ({} !~ {}).'.format(function['php'], phpdoc_type))


def validate_functions(functions):
  for function in functions:
    print ("Fonction : {}".format (function))
    if function[0:3] == "get":
      validate_getter(functions[function])
    elif function[0:3] == "set":
      validate_setter(functions[function])

def main(phpcode):
  sanitized_code = extract_attributes_and_functions_and_phpdoc_from_phpcode(phpcode)
  validate_attributes(sanitized_code['attributes'])
  validate_functions(sanitized_code['functions'])

if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Validation de la cohérence entre les types doctrine annotés & les types php.")
  parser.add_argument ('-f', '--file', type = str, \
      help = "Emplacement du fichier php à vérifier.", \
      dest = "file", required = True)
  args = parser.parse_args ()

  main(load_data_from_file(args.file))
  
