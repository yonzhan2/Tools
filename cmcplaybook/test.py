import yaml
import os

base_dir = ''
yaml_load = yaml.safe_load(open(os.path.join(base_dir, 'cmcversion.yml')))
yaml_data = yaml_load.get('component')
print(yaml_data)
