#!/usr/bin/env python
import argparse

def generate_xetters (attribute):
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
    }}
""".format (attribute, getterName, attribute, setterName, attribute, attribute, attribute)
  return result

if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Génération des Xetters.")
  parser.add_argument ('--attribute', type = str, \
      help = "Nom de l'attribut.", \
      dest = "attr", required = True)
  args = parser.parse_args ()
  print (generate_xetters (args.attr))
