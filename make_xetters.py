#!/usr/bin/env python
import argparse

def generate_xetters (attribute, is_array):
  saneAttribute = "".join ([ u.capitalize () for u in attribute.split ('_') ])

  getterName = "get{}".format (saneAttribute)
  setterName = "set{}".format (saneAttribute)
  result = """
    private ${};
    public function {} ()
    {{
        return $this->{};
    }}
    public function {} (${})
    {{
        $this->{} = ${};
        return $this;
    }}""".format (attribute, getterName, attribute, setterName, attribute, attribute, attribute)

  if is_array:
    adderName = "add{}".format (saneAttribute)
    result = """{}
    public function {} (${})
    {{
        $this->{}[] = ${};
        return $this;
    }}""".format (result, adderName, attribute, attribute, attribute)
  return result

if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Génération des Xetters.")
  parser.add_argument ('-a', '--attribute', type = str, \
      help = "Nom de l'attribut.", \
      dest = "attr", required = True)
  parser.add_argument ('-i', '--is-array', \
      help = "Activer si l'attribut est un tableau.", \
      dest = "is_array", required = False, action = 'store_true')
  args = parser.parse_args ()
  print (generate_xetters (attribute = args.attr, is_array = args.is_array))
