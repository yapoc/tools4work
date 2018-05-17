#!/usr/bin/env python
import argparse
import sys
import json
from libs import load_data_from_file, save_to_file, \
       extract_attributes_from_php_code, extract_classname_from_php_code, \
       make_random_data_from_attributes

def _write_behat_assertions_based_on_data (data):
  result = ""
  for k in data:
    result += """    And the JSON node "{}" should contain "{}"\n""".format (k, data[k])
  return result

def php_code_to_behat_feature (php_code):
  attributes = extract_attributes_from_php_code (php_code)
  classname = extract_classname_from_php_code (php_code)
  endpoint = '/api/{}s'.format (classname.lower ())

  posted_data = make_random_data_from_attributes (attributes, "POST CONTEXT")
  posted_data_assertions = _write_behat_assertions_based_on_data (posted_data)

  putted_data = make_random_data_from_attributes (attributes, "PUT CONTEXT")
  putted_data_assertions = _write_behat_assertions_based_on_data (putted_data)

  data = {
    'endpoint': endpoint,
    'classname': classname,
    'posted_json': json.dumps (posted_data, sort_keys = True, indent = 2),
    'putted_json': json.dumps (putted_data, sort_keys = True, indent = 2)
  }


  result = """
@admin @{endpoint} @api
Feature: {classname}
  In order to use the application
  I need to be able to retrieve a collection of {classname} resources through the API.
  I need to be able to create a new {classname} resource through the API.
  I need to be able to access an existing {classname} resource through the API.
  I need to be able to update an existing {classname} resource through the API.
  I need to be able to delete an existing {classname} resource through the API.\n""".format (**data)

  result += """
  Scenario: Retrieve a collection of {classname} resources
    When I go to "{endpoint}"
    Then the response status code should be 200
    And the response should be in JSON
    And the header "Content-Type" should be equal to "application/json; charset=utf-8"\n""".format (**data)

  result += """
  Scenario: Create a new {classname}
    When I send a "POST" request to "{endpoint}" with body:
    \"\"\"
{posted_json}
    \"\"\"
    Then the response status code should be 201
    And the response should be in JSON
    And the header "Content-Type" should be equal to "application/json; charset=utf-8"\n""".format (**data)
  result += posted_data_assertions

  result += """
  Scenario: Access recently created {classname}
    Given I have a "{endpoint}" containing:
    \"\"\"
{posted_json}
    \"\"\"
    When I send a "GET" request to "{endpoint}/__ID__"
    Then the response status code should be 200
    And the response should be in JSON
    And the header "Content-Type" should be equal to "application/json; charset=utf-8"\n""".format (**data)
  result += posted_data_assertions

  result += """
  Scenario: Update recently created {classname}
    Given I have a "{endpoint}" containing:
    \"\"\"
{posted_json}
    \"\"\"
    When I send a "PUT" request to "{endpoint}/__ID__" with body:
    \"\"\"
{putted_json}
    \"\"\"
    Then the response status code should be 200
    And the response should be in JSON
    And the header "Content-Type" should be equal to "application/json; charset=utf-8"\n""".format (**data)
  result += putted_data_assertions

  result += """
  Scenario: Delete recently created {classname}
    Given I have a "{endpoint}" containing:
    \"\"\"
{posted_json}
    \"\"\"
    When I send a "DELETE" request to "{endpoint}/__ID__"
    Then the response status code should be 204
    And the response should be empty\n""".format (**data)
  return result

if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Joli reformattage de documents json.")
  parser.add_argument ('-f', '--file', type = str, \
      help = "Emplacement du fichier php pour lequel il faut écrire les fonctions de test.", \
      dest = "file", required = False)
  parser.add_argument ('-i', '--stdin', action = 'store_true', \
      help = "On écrit les fonctions depuis le code envoyé sur la console.",
      dest = "from_stdin", default = True)
  args = parser.parse_args ()

  if args.file:
    outfile = args.file.replace ('.php', '.feature').lower ()
    save_to_file (outfile, php_code_to_behat_feature (load_data_from_file (args.file)))
    print ("Le fichier {} a été correctement créé.".format (outfile))
  elif args.from_stdin:
    print (php_code_to_behat_feature (sys.stdin.read ()))
