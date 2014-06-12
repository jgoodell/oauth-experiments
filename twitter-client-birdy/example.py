from json import (dumps,
                  loads,
                  )
from pprint import pprint
from ConfigParser import RawConfigParser

from birdy.twitter import UserClient

config = RawConfigParser()
try:
    config.read('conf.cfg')
except Exception, e:
    print(e)
    print("You need to set your consumer and access values in a conf.cfg file.")
    print("Here you go...")
    with open('conf.cfg', 'wb') as configfile:
        config.write(configfile)
    sys.exit(1)

#CONSUMER_KEY = '17BpmHHtNJynm3MaKrGU4iXbB'
#CONSUMER_SECRET = 'ebGbtZOCoXLOXFgMg8bEGi3KaRIQKmQ2mlO9eQUAkNq0wWZeEg'
#ACCESS_TOKEN = '2561543448-WZy6Mks50SyY8iVM3wQiM2ZZ3D2VWDffPzf1yf9'
#ACCESS_TOKEN_SECRET = 'rMQjNwedaxsVgJNNCQiSuV8YMv8PKcz48CcJPluX7xYWG'

import pdb; pdb.set_trace()

CONSUMER_KEY = config.get('consumer','key')
CONSUMER_SECRET = config.get('consumer','secret')
ACCESS_TOKEN = config.get('access','token')
ACCESS_TOKEN_SECRET = config.get('access','secret')

print(CONSUMER_KEY)
print(CONSUMER_SECRET)
print(ACCESS_TOKEN)
print(ACCESS_TOKEN_SECRET)

client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)

response = client.api.users.show.get(screen_name='jasongoodell1')
pprint(loads(dumps(response.data)))
