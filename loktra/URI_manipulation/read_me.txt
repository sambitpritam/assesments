packages used:
	subprocess

Usage:

from URL_manipulation import *

# aa = URLManip('<url path in quotes>')
aa = URLManip('https://www.youtube.com/watch?v=OLuWHr6-0YQ&list=RDxyqQ4iT4IeU&index=27')

aa.split() 		# split all the components of the provided url.
aa.replace(key, replace_value)		# key = {scheme, netloc, port, path, parameters, query, fragment}
aa.is_valid()	# validates if the provided url is a valid url or not.
aa.add()		# adds a new item to the url dictionary
aa.get(key)		# get the value of the requested key in the given url
aa.get_domain()	# get the domain name from the provided url.

generate_url(scheme, netlocation, port, path, parameters, query, fragment)	# if any of the provided parameters is not reuqired in the URL, specify 'null' in its location. NOTE: port parameter takes only integer value.