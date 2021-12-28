import os
from arcgis.gis import GIS
import argparse

import creds


def update_ipynb(ipynb_file, gis, agol_id=None, item_properties=None):
    fname = os.path.basename(ipynb_file).split('.')[0]
    item = None
    # if agol_id then update existing
    if agol_id:
        item = gis.content.get(agol_id)
    else:
        search = gis.content.search(f"title:{fname}", item_type='Notebook')
        if search:
            item = search[0]
    if item:
        # update
        print('updating existing notebook')
        item.update(data=ipynb_file, item_properties=item_properties)
    else:
        if not item_properties:
            item_properties = {'title': fname,
                          'type': 'Notebook',
                               'tags': f'{fname},notebook,autodeploy'}
        print('creating new notebook')
        item = gis.content.add(item_properties=item_properties, data=ipynb_file)
    return item

# todo - share with notebook group

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('agol_un', help='AGOL/Geoplatform username')
    parser.add_argument('agol_pw', help='AGOL/Geoplatform password')
    parser.add_argument('ipynb_file', help='relative path to ipynb file')
    args = parser.parse_args()
    print(f'username: {args.agol_un}')
    print(f'password: {args.agol_pw}')
    un = creds.un
    pw = creds.pw
    gis = GIS(username=un, password=pw)
    update_ipynb(ipynb_file='C:\Data\Py2Notebook\R9_Fires_Notebook_TestUpdate.ipynb', gis=gis)

if __name__ == '__main__':
    main()
