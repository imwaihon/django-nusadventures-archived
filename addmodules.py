import json
import os


json_data=open('moduleList.json').read()

data = json.loads(json_data)

def populate(info):
	for key, value in info.items():
		FixedModule.objects.get_or_create(code=key, name=value, description="")
		print(key)

if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nusadventures.settings')
    from taskgoals.models import FixedModule
    populate(data)
