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

def convert_doctrine_to_php_type(doctrine_type):
  mapping = {
    'integer': 'int',
    'text': 'string',
    'string': 'string',
    'boolean': 'bool',
    'datetime': '\\DateTime'
  }
  if doctrine_type in mapping:
    return mapping[doctrine_type]
  return "Type {} inconnu".format(doctrine_type)

def convert_doctrine_declaration_to_phptype(doctrine):
  doctrine_type = convert_doctrine_to_php_type(doctrine['type'])
  if 'nullable' in doctrine and doctrine['nullable'] == 'true':
    doctrine_type = "?{}".format(doctrine_type)

  return doctrine_type

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

def validate_getter(function):
  function['php'] = re.sub('^\s*:\s*', '', function['php'])
  if is_attribute_same_in_phpcode_and_phpdoc(function['php'], function['phpdoc']):
    return "OK"
  else:
    return "KO"

def validate_setter(function):
  phpdoc_type = function['phpdoc'][list(function['phpdoc'].keys())[0]].strip()
  function['php'] = function['php'].strip()

  if is_attribute_same_in_phpcode_and_phpdoc(function['php'], phpdoc_type):
    return "OK"
  else:
    return "KO"

def is_phpdoc_attribute_nullable(phpdoc):
  result = (False, "KO")
  if phpdoc.endswith('|null'):
    result = (True, "OK")

  return result

def is_phpcode_attribute_nullable(phpcode):
  result = (False, "KO")
  phpcode = re.sub('^\s*:\s*', '', phpcode)
  if phpcode.startswith('?'):
    result = (True, "OK")

  return result

def correlate(functions, attributes):
  for attr in attributes:
    getter = "get{}{}".format(attr[:1].upper(), attr[1:])
    setter = "set{}{}".format(attr[:1].upper(), attr[1:])
    doctrine_converted_type = convert_doctrine_declaration_to_phptype(attributes[attr]['doctrine'])

    print ("+-{:-^66}-+".format('-'))
    print ("| {: ^66} |".format(attr))
    print ("+-{:-^25}-+-{:-^25}-+-{:-^10}-+".format("-", "-", "-"))

    print("| {:>25} | {:>25} | {:^10} |".format("Getter nullable php doc", "", is_phpdoc_attribute_nullable(functions[getter]['phpdoc'])[1]))
    print("| {:>25} | {:>25} | {:^10} |".format("Getter nullable php code", "", is_phpcode_attribute_nullable(functions[getter]['php'])[1]))

    print("| {:>25} | {:>25} | {:^10} |".format("Getter php code", "Getter php doc", validate_getter(functions[getter])))

    temp = "KO"
    if doctrine_converted_type == attributes[attr]['phpdoc']:
      temp = "OK"
    print("| {:>25} | {:>25} | {:^10} |".format("Php code", "Doctrine annotation", temp))

    temp = "KO"
    if doctrine_converted_type == functions[getter]['php']:
      temp = "OK"
    print("| {:>25} | {:>25} | {:^10} |".format("Doctrine annotation", "Getter php code out", temp))

    if setter in functions:
      print("| {:>25} | {:>25} | {:^10} |".format("Setter php code", "Setter php doc", validate_setter(functions[setter])))

      temp = "KO"
      if doctrine_converted_type == functions[setter]['php']:
        temp = "OK"
      print("| {:>25} | {:>25} | {:^10} |".format("Doctrine annotation", "Setter php code in", temp))
  print ("+-{:-^66}-+".format('-'))

def main(phpcode):
  sanitized_code = extract_attributes_and_functions_and_phpdoc_from_phpcode(phpcode)
  correlate(sanitized_code['functions'], sanitized_code['attributes'])

if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Validation de la cohérence entre les types doctrine annotés & les types php.")
  parser.add_argument ('-f', '--file', type = str, \
      help = "Emplacement du fichier php à vérifier.", \
      dest = "file", required = True)
  args = parser.parse_args ()

  main(load_data_from_file(args.file))
  
