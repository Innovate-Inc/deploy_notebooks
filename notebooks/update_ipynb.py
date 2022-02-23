import os
from arcgis.gis import GIS
import argparse
import jupytext

def clean_py_script(input_py, output_py=None):
    f = open(input_py, 'r').read()
    lines = f.split('\n')
    clean = '\n'.join([l for l in lines if not l.startswith('pip') and not l.startswith('main()')])
    # fname = input_py.replace('.py', '_clean.py')
    fname = 'cleaned_notebook.py' if not output_py else output_py
    with open(fname, 'w') as f:
        f.write(clean)
    return fname


def update_ipynb(input_file, agol_un, agol_pw, agol_id=None, item_properties=None, input_func=[]):
    if input_func is None:
        input_func = []
    gis = GIS(username=agol_un, password=agol_pw)
    py_script = open(input_file, 'r')
    py_script_contents = py_script.read()
    py_script.close()
    lines = py_script_contents.split('\n')
    if input_func:
        for func_file in input_func:
            import_line = [l for l in lines if func_file.split('.')[0] in l and 'import' in l]
            if import_line:
                import_line = import_line[0]
                with open(func_file, 'r') as file:
                    file_contents = file.read()
                    edits = py_script_contents.replace(import_line, '\n'+file_contents+'\n')
                    with open(input_file, 'w') as py_script:
                        py_script.write(edits)

                # file.close()
    # f.close()

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


# def get_agol_token(username, password):
#     gis = GIS(username=username, password=password)
#     token = gis._con.token
#     if not token:
#         raise Exception('no valid token')
#     return token


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

