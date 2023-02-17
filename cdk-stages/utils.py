import os
import string
import sys
from re import sub


def create_file(template_path, target_path, params={}):
    with open(os.path.abspath(os.path.dirname(__file__) + "/" + template_path)) as t:
        template = string.Template(t.read())
    index = template.substitute(**params)
    with open(target_path, "w") as output:
        output.write(index)


def camel_case(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return ''.join(string)
