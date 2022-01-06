import os
from arcgis.gis import GIS
import argparse
import jupytext
import re

def clean_py_script(input_py):
    f = open(input_py, 'r').read()
    lines = f.split('\n')
    clean = '\n'.join([l for l in lines if not l.startswith('pip') and not l.startswith('main()')])
    fname = input_py.replace('.py', '_clean.py')
    with open(fname, 'w') as f:
        f.write(clean)
    return fname


def update_ipynb(input_file, gis, agol_id=None, item_properties=None):
    fname = os.path.basename(input_file).split('.')[0]
    if os.path.basename(input_file).split('.')[1] == "py":
        input_py = jupytext.read(input_file)
        ipynb_name = fname + '.ipynb'
        jupytext.write(input_py, ipynb_name)
        input_file = input_file.replace(os.path.basename(input_file), ipynb_name)
        fname = os.path.basename(input_file).split('.')[0]
    print(fname)
    item = None
    # if agol_id then update existing
    if agol_id:
        item = gis.content.get(agol_id)
    else:
        search = gis.content.search(f"title:{fname}", item_type='Notebook')
        search = [x for x in search if x.title == fname]
        if search:
            item = search[0]
    if item:
        # update
        print(f'updating existing notebook {item.title}')
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
    parser.add_argument('notebook_file', help='relative path to ipynb or py file')
    args = parser.parse_args()
    gis = GIS(username=args.agol_un, password=args.agol_pw)
    update_ipynb(input_file=args.notebook_file, gis=gis)

if __name__ == '__main__':
    main()

