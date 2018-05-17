#!/usr/bin/env python
import argparse
import sys
from libs import load_data_from_file, save_to_file, extract_attributes_from_php_code

def php_code_to_xetters (php_code):
  attributes = {}
  for attribute in extract_attributes_from_php_code (php_code):
    functionSuffix = "{}{}".format (attribute[:1].upper (), attribute[1:])
    attributes[attribute] = {
      'getter': "get{}".format (functionSuffix),
      'setter': "set{}".format (functionSuffix),
      'tester': "test{}".format (functionSuffix),
    }
          
  result = """<?php
namespace App\Tests\Entity;
use PHPUnit\Framework\TestCase;
use App\Entity\XXX;

class XXXTest extends TestCase
{
    public function setUp (): void
    {
      $this->entity = new XXX ();
      $token = rand (0, 10000000);
"""
  for a in attributes:
    result += """
      $this->{} = "Valeur de test pour {} - $token.";""".format (a, a)
  result += """
    }"""

  for a in attributes:
    result += """
    public function {} ():void
    {{
        $this->entity->{} ($this->{});
        $this->assertEquals ($this->{}, $this->entity->{} ());
    }}""".format (attributes[a]['tester'], attributes[a]['setter'], a, a, attributes[a]['getter'])
  result += """
}"""
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
    outfile = args.file.replace ('.php', 'Test.php')
    save_to_file (outfile, php_code_to_xetters (load_data_from_file (args.file)))
    print ("Le fichier {} a été correctement créé.".format (outfile))
  elif args.from_stdin:
    print (php_code_to_xetters (sys.stdin.read ()))
