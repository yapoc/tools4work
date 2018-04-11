#!/usr/bin/env python
import argparse
import sys
from libs import load_data_from_file, json2yaml, save_to_file

if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Joli reformattage de documents json.")
  parser.add_argument ('-f', '--file', type = str, \
      help = "Emplacement du fichier json à convertir.", \
      dest = "file", required = False)
  parser.add_argument ('-i', '--stdin', action = 'store_true', \
      help = "On convertit d'après la ligne de commande.", \
      dest = "from_stdin", default = True)
  args = parser.parse_args ()
  if args.file:
    outfile = args.file.replace ('json', 'yaml').replace ('js', 'yaml')
    save_to_file (outfile, json2yaml (load_data_from_file (args.file)))
    print ("Le fichier {} a été correctement créé.".format (outfile))
  elif args.from_stdin:
    print (json2yaml (sys.stdin.read ()))
