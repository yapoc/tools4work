#!/usr/bin/env python
import argparse
import sys

def main(constName):
  constElements = constName.split('_')
  attributeName = ''
  xetter_suffix = ''
  for elt in constElements:
    if attributeName == "":
      attributeName = elt.lower()
      xetter_suffix = elt.capitalize()
    else:
      attributeName = "{}{}".format(attributeName, elt.capitalize())
      xetter_suffix = "{}{}".format(xetter_suffix, elt.capitalize())

  print("""    /**
     * @ORM\Column(type='string', length=255)
     *
     * @Dump\Column
     *
     * @var string
     */
    private ${};

    /**
     * @return string
     */
    public function get{}():string
    {{
        return $this->{};
    }}

    /**
     * @param string ${}
     *
     * @return self
     */
    public function set{}(string ${}): self
    {{
        return $this;
    }}
""".format(attributeName, xetter_suffix, attributeName, attributeName, xetter_suffix, attributeName));

if __name__ == "__main__":
  parser = argparse.ArgumentParser ( description = "Conversion d'une constante en snake case majuscule en attribut + Xetters PHP.")
  parser.add_argument ('-c', '--const', type = str, \
      help = "Nom de la constante.", \
      dest = "const", required = True)
  args = parser.parse_args ()
  main(args.const)
