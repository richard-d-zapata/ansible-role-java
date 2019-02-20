import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def get_java_version():
    return os.getenv('JAVA_VERSION', '11.0.2')


@pytest.fixture(scope='module')
def test_vars(host):
    java_version = get_java_version()
    java_version_parts = java_version.split('.')

    java_version_feature = java_version_parts[0]
    if len(java_version_parts) > 1:
        java_version_interim = java_version_parts[1]
    else:
        java_version_interim = '0'
    if len(java_version_parts) > 2:
        java_version_update = java_version_parts[2]
    else:
        java_version_update = '0'
    if len(java_version_parts) > 3:
        java_version_patch = java_version_parts[3]
    else:
        java_version_patch = '0'

    java_version_string = ''
    if int(java_version_feature) > 8:
        if int(java_version_patch) > 0:
            java_version_string = '.' + java_version_patch + java_version_string
        if (int(java_version_update) > 0) or (java_version_string != ''):
            java_version_string = '.' + java_version_update + java_version_string
        if (int(java_version_interim) > 0) or (java_version_string != ''):
            java_version_string = '.' + java_version_interim + java_version_string
        java_version_string = java_version_feature + java_version_string
        java_version_string_short = java_version_string
    else:
        if int(java_version_patch) > 0:
            java_version_string = '.' + java_version_patch + java_version_string
        if (int(java_version_update) > 0) or (java_version_string != ''):
            java_version_string = '-b' + java_version_update + java_version_string
        if (int(java_version_interim) > 0) or (java_version_string != ''):
            java_version_string = '_' + java_version_interim + java_version_string
        else:
            java_version_string = '_0' + java_version_string
        java_version_string = '1.' + java_version_feature + java_version_string
        java_version_string_short = java_version_feature + 'u' + java_version_interim

    test_vars = {
        'java_version': java_version,
        'java_version_short': java_version_string_short,
    }
    return test_vars


def test_java_version_installed(host, test_vars):
    os = host.system_info.distribution
    if os == 'Windows':
        result = host.run("java.exe -version")
    else:
        result = host.run("java -version")
    assert test_vars['java_version'] in result.stderr
