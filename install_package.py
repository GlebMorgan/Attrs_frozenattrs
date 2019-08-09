import re
from os import walk, listdir, linesep
from subprocess import run
from os.path import join as joinpath, isfile


PACKAGE = 'attrs'
PATH = 'src/attr'


version_id_pattern = r'([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?' \
                     r'(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?'


def die(msg, errcode=1):
    if isinstance(msg, int): errcode, msg = msg, ''
    print(msg)
    input('Press any key to exit ...')
    exit(errcode)


def ask(msg, options=None):
    if not options:
        options = ['y', 'n']
    options = list(options)
    choices = f"{msg} [{', '.join((name if name else '<Enter>' for name in options))}]: "
    for i, string in enumerate(options): options[i] = string.lower()
    for _ in range(10):
        ans = input(choices)
        if ans.strip().lower() in options: return ans
    else: die("Run out of attempts")


def handle_errors(result):
    if result.returncode > 0:
        print()
        print("ERROR!")
        if ask("Continue?") != 'y': die("Cancelled")
    else:
        print()
        print("OK")


def get_version():
    with open(PATH + '/__init__.py') as file:
        version = re.search(rf'__version__ = "({version_id_pattern})"', file.read(), re.S).group(1)
        print(f"version: {version}")
        if version is None: die("No valid version id found in __init__.py")
        return version


def cmd(command):
    return run(args=command, capture_output=False, encoding='oem')


def install(version):

    uninstall_command = dict(
            command=rf"pip uninstall {PACKAGE}",
            msg='Uninstalling old package ...',
    )
    install_command = dict(
            command=rf"pip install --upgrade --no-index --find-links ./dist {PACKAGE}=={version}",
            msg='Installing new package ...',
    )

    for action in (install_command, ):
        print(action['msg'])
        handle_errors(cmd(action['command']))


def check_wheel_overwrite(version):
    files = [f for f in listdir('dist')]
    for filename in files:
        if version in filename and filename.endswith('.whl'):
            print(f"File with current version number ({version}) already exists: {filename}")
            if ask("Overwrite?") == 'y': return True
            else: die("Cancelled. Change version number in __init__.py")
    return False


def build(version):
    overwrite = check_wheel_overwrite(version)
    handle_errors(cmd(r"python setup.py bdist_wheel"))
    return overwrite


if __name__ == '__main__':
    try:
        print(f"Package: {PACKAGE}")
        print('-'*120)
        print()
        startup_msg = "Enter - build & install, B - build, I - install"
        reply = ask(startup_msg, ('', 'B', 'I')).upper()
        ver = get_version()
        if reply == '' or reply == 'B':
            owrt = build(ver)
            print(f"Overwritten: {'yes' if owrt else 'no'}")
        if reply == '' or reply == 'I':
            print(f"Press any key to reinstall PyUtils v{ver} ...")
            install(ver)
        print()
    except Exception as e:
        die("ERROR!" + linesep + str(e))
    else:
        die("DONE!", 0)
