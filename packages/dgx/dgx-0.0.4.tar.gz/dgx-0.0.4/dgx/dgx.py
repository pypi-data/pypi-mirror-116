from os import makedirs, path, listdir, system
from werkzeug.utils import secure_filename
import shutil


def create_file(sfilepath: str, dfilepath: str, props: dict):
    """Lee archivo original, reemplaza las variables y crea archivo de salida"""
    with open(sfilepath, "r") as fl:
        data = fl.read()
        for prop, value in props.items():
            data = data.replace(prop, value)
    with open(dfilepath, "w") as fl:
        fl.write(data)


def create_virtual_env(name: str, rootProject: str, rootApi: str):
    """
    Crea entorno virtual e instala las dependencias
    """
    rootApi = rootApi.replace(rootProject + '/', './')  # quita la carpeta raiz
    system("""
        cd {1};
        python3 -m venv {0}-venv;
        source {0}-venv/bin/activate;
        pip install --upgrade pip;
        pip install -r {2}/requirements.txt;
    """.format(name, rootProject, rootApi))


def delete_app(napp: str):
    """
    Elimina el directorio
    """
    if napp:
        napp = secure_filename(napp).lower().replace('-api', '') + '-project'
        if input('Are you sure you want to delete the %s (Y/N): ' % napp).lower() == 'y':
            shutil.rmtree(napp)
    else:
        print("you need to specify the api name")


def create_app(napp: str):
    """
    Crea app
    """
    if napp:
        CDIR = path.dirname(path.realpath(__file__))
        acode = input('app code: ').strip()
        port = input('app port: ').strip() or '5000'
        napp = secure_filename(napp).lower().replace('-api', '')
        rootProject = napp + '-project'  # carpeta de proyecto
        rootPath = path.join(rootProject, napp + '-api')  # carpeta del api
        # crea carpetas
        for dname in ('', 'modules', 'resources', '__temp__'):
            print("creating > " + (dname or rootPath))
            makedirs(path.join(rootPath, dname))
        DRESOURCES = path.join(CDIR, 'resources')
        for name in listdir(DRESOURCES):
            if name != '__pycache__':
                print("creating > " + name)
                npath = path.join(DRESOURCES, name)
                if path.isdir(npath):  # si es directorio lo copia todo
                    shutil.copytree(npath, path.join(rootPath, name), dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                else:  # si es un archivo
                    if name == 'const.py':
                        create_file(npath, path.join(rootPath, name), {'<<APPLICATION_CODE>>': acode, '<<PORT>>': port})
                    elif name == 'app.py':
                        create_file(npath, path.join(rootPath, name), {'<<API_NAME>>': napp})
                    elif name == 'runServer.py':
                        create_file(npath, path.join(rootPath, name), {'<<API_NAME>>': napp})
                    elif name.endswith('.pyc') is False:
                        shutil.copyfile(npath, path.join(rootPath, name))
        create_virtual_env(napp, rootProject, rootPath)  # crea entorno e instala dependencias
        print("\n\nhappy coding\n\n")
    else:
        print("you need to specify the api name")
