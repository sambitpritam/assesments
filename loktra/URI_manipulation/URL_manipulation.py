'''
    This file will be used as a import package in other apps to use its features. all its features are
    created using the native python. No external packages are being used to handle the manipulations of URLs and URIs

    The var names used in this application is used keeping in mind the variable names of the specific items in the URLs based on the
    specific packages like urllib and other.

    URLs: scheme://netlocation:80/path;parameters?query#fragment
'''

import subprocess as s


class URLManip:

    def __init__(self, url):
        self.url = url

    def split(self):
        url_component = {}
        url = self.url
        url_lst = url.split('://')
        url_component['scheme'] = url_lst[0]
        post_scheme = url_lst[1]
        netloc_other = post_scheme.split('/', 1)
        url_component['netloc'] = netloc_other[0]
        in_netloc = netloc_other[0]
        if ':' in in_netloc:
            address_port = in_netloc.split(':')
            url_component['port'] = address_port[1]
        path_other = netloc_other[1]
        # path_other = post_netloc.split(';')
        if ((';' in path_other) or ('?' in path_other) or ('#' in path_other)):
            if (';' in path_other):
                url_component['path'] = path_other.split(';')[0]
                if (('?' in path_other.split(';')[1]) or ('#' in path_other.split(';')[1])):
                    if ('?' in path_other.split(';')[1]):
                        url_component['parameters'] = path_other.split(';')[1].split('?')[0]
                        if '#' in path_other.split(';')[1].split('?')[1]:
                            url_component['query'] = path_other.split(';')[1].split('?')[1].split('#')[0]
                            url_component['fragment'] = path_other.split(';')[1].split('?')[1].split('#')[1]
                        else:
                            url_component['query'] = path_other.split(';')[1].split('?')[1]
                    else:
                        url_component['parameters'] = path_other.split(';')[1].split('#')[0]
                        url_component['fragment'] = path_other.split(';')[1].split('#')[1]
                        # statements for tru condition
                else:
                    url_component['parameters'] = path_other.split(';')[1]
            elif ('?' in path_other):
                url_component['path'] = path_other.split('?')[0]
                if ('#' in path_other.split('?')[1]):
                    url_component['query'] = path_other.split('?')[1].split('#')[0]
                    url_component['fragment'] = path_other.split('?')[1].split('#')[1]
                else:
                    url_component['query'] = path_other.split('?')[1]
            elif ('#' in path_other):
                url_component['path'] = path_other.split(';')[0]
                url_component['fragment'] = path_other.split(';')[1]
        else:
            url_component['path'] = path_other[0]

        # if ';' in post_netloc:
        #     post_path = path_other[1]
        #     params_other = post_path.split('?')
        #     url_component['parameters'] = params_other[0]
        #     if '?' in post_path:
        #         post_params = params_other[1]
        #         query_fragment = post_params.split('#')
        #         url_component['query'] = query_fragment[0]
        #         if '#' in post_params:
        #             url_component['fragment'] = query_fragment[1]

        return url_component

    def replace(self, key, replace_value):
        url_components = self.split()
        key_exists = url_components.get(key) or False

        if key_exists:
            url_components[key] = replace_value
            return self.regen(**url_components)
        else:
            return 'Error: selected key does not exist in the supplied URL'

    def is_valid(self):
        url = self.url

        if s.call(['ping', url]) == 0:
            return True
        else:
            return False

    def add(self, key, value):
        url_components = self.split()
        url_components[key] = value

        return self.regen(**url_components)

    def get(self, key):
        url_components = self.split()
        try:
            return url_components.get(key)
        except:
            return 'Error: Invalid Key requested'

    def get_domain(self):
        url_components = self.split()
        return url_components['netloc']

    def regen(self, **url_component):
        url = ''
        if url_component['scheme'] is not None:
            url +=  url_component['scheme'] + '://'
        if url_component['netloc'] is not None:
            url +=  url_component['netloc']
        if url_component['port'] is not None:
            url += ':' + str(url_component['port'])
        if url_component['path'] is not None:
            url += '/' + url_component['path']
        if url_component['parameters'] is not None:
            url += '/;' + url_component['parameters']
        if url_component['query'] is not None:
            url += '/?' + url_component['query']
        if url_component['fragment'] is not None:
            url += '/#' + url_component['fragment']

        return url

#
# def generate_url(scheme, netlocation, port, path, parameters, query, fragment):
#     # scheme://netlocation:80/path;parameters?query#fragment
#     if scheme != 'null' and netlocation != 'null' and port != 'null' and path != 'null' and parameters != 'null' and query != 'null' and fragment != 'null':
#         url = scheme + '://' + netlocation + ':' + port +'/' + path + ';' + parameters + '?' + query + '#' + fragment
#         return url
#     else:
#         # Default scheme is http: unless https: is provided
#         if scheme != 'null':
#             f_scheme = scheme + ':'
#         else:
#             f_scheme = 'http:'
#         #     Domain name cannot be null
#         if netlocation != 'null':
#             f_netlocation = '//' + netlocation
#         else:
#             return 'ERROR: Domain cannot be null...'
#         # check if port value exits
#         if port != 'null':
#             if isinstance(port, int):
#                 f_port = ':' + port
#             else:
#                 return 'ERROR: Port number needs to be an integer'
#         else:
#             f_port = None
#         # check if path exists
#         if path != 'null':
#             f_path = '/' + path
#         else:
#             f_path = None
#         # check if parameters exist
#         if parameters != 'null':
#             f_parameters = ';' + parameters
#         else:
#             f_parameters = None
#         # check if query exist
#         if query != 'null':
#             f_query = '?' + query
#         else:
#             f_query = None
#         # check if fragment exist
#         if fragment != 'null':
#             f_fragment = '#' + fragment
#         else:
#             f_fragment = None
#
#     return f_scheme + f_netlocation + f_port + f_path + f_parameters + f_query + f_fragment