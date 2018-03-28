# tools4work
Some tools that may be useful when I'm at work.

## `check_yaml_file_validity.py`
This file uses the `PyYAML` python library to check a file seems to be a valid `yaml` one. Don't forget to install the package in your environment before launching the script!

## `make_xetters.py`
A simple `python` script that creates getters and setters for a given attribute.
```sh
[user@host ~] ./make_xetters.py --attribute my_special_attr
    private $my_special_attr;
    public function getMySpecialAttr ()
    {
        return $this->my_special_attr;
    }
    public function setMySpecialAttr ($my_special_attr)
    {
        $this->my_special_attr = $my_special_attr;
        return $this;
    }

```
