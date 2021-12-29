import os
from arcgis.gis import GIS
import argparse
import jupytext


def update_ipynb(input_file, gis, agol_id=None, item_properties=None):
    fname = os.path.basename(input_file).split('.')[0]
    if os.path.basename(input_file).split('.')[1] == "py":
        input_py = jupytext.read(input_file)
        ipynb_name = fname + '.ipynb'
        jupytext.write(input_py, ipynb_name)
        input_file = input_file.replace(fname, ipynb_name)

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
        item.update(data=input_file, item_properties=item_properties)
    else:
        if not item_properties:
            item_properties = {'title': fname,
                          'type': 'Notebook',
                               'tags': f'{fname},notebook,autodeploy'}
        print('creating new notebook')
        item = gis.content.add(item_properties=item_properties, data=input_file)
    return item

# todo - share with notebook group

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('agol_un', help='AGOL/Geoplatform username')
    parser.add_argument('agol_pw', help='AGOL/Geoplatform password')
    parser.add_argument('ipynb_file', help='relative path to ipynb file')
    args = parser.parse_args()
    print("_".join([x for x in args.agol_un]))
    print(f'username: {args.agol_un}')
    print(f'password: {args.agol_pw}')
    gis = GIS(username=args.agol_un, password=args.agol_pw)
    # update_ipynb(ipynb_file='C:\Data\Py2Notebook\R9_Fires_Notebook_TestUpdate.ipynb', gis=gis)
    update_ipynb(input_file=args.ipynb_file, gis=gis)

if __name__ == '__main__':
    main()
