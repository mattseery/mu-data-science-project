import yaml

__CONFIG__ = None

def get_config(filename='config.yml'):
    global __CONFIG__
    if __CONFIG__ is None:
        with open(filename, encoding='utf-8') as f:
            contents = f.read()

            __CONFIG__ = yaml.load(contents)
    return __CONFIG__

