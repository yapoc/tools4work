#!/usr/bin/env python
import argparse
import json
import sys
from libs import load_data_from_file, reformat_json, save_to_file

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
