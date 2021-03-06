# tools4work
Some tools that may be useful when I'm at work.

## `make_test_php_xetters.py`
This script parses some PHP code or script and tries to write automatic test functions.

## `json2yaml.py`
This script converts from `json` to `yaml`. Works at file level or using inputs from `stdin`.

## `.bashrc`
Two functions to ease the manipulation of an API : 
  * `api_get ENDPOINT` uses `pretty_json.py` to nicely display the response of the server.
  * `api_post ENDPOINT JSON_FILE` `POST`s the data contained in `JSON_FILE` then uses `pretty_json.py` to nicely display the response of the server.

## `pretty_json.py`
This script cleans and indent a json file. If no argument, gets inputs from `stdin` : 

```sh
[user@host ~] echo '{"a":"b", "c":1}' | pretty_json.py
{
  "a": "b",
  "c": 1
}
```
or 
```sh
[user@host ~] echo '{"a":"b", "c":1}' > /tmp/file
[user@host ~] pretty_json.py -f /tmp/file 
Le fichier a été correctement réécrit.
[user@host ~] cat /tmp/file 
{
  "a": "b",
  "c": 1
}
```

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

## `.vimrc`
My `.vimrc` file.
