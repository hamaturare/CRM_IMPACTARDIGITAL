# This file contains the WSGI configuration required to serve up your
# web application at http://fmendes.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#

# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# getting imports and sys.path right can be fiddly!
# We've tried to collect some general tips here:
# https://help.pythonanywhere.com/pages/DebuggingImportError


# +++++++++++ DJANGO +++++++++++
import os
import sys

# Caminho para o diretório onde manage.py reside
project_home = '/home/fmendes/CRM_IMPACTARDIGITAL'
if project_home not in sys.path:
    sys.path.append(project_home)

# Caminho para o diretório onde settings.py reside
project_settings = os.path.join(project_home, 'CRM_ID')
if project_settings not in sys.path:
    sys.path.append(project_settings)

os.environ['DJANGO_SETTINGS_MODULE'] = 'CRM_ID.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()