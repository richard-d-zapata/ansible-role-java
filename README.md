# Kaos2oak Java

Install Java

This Ansible role is intended to install Java for testing purposes. No attempt
is made to "harden" the installation for production use.

Currently, this role supports installation of OpenJDK (of the Amazon Corretto
or RedHat flavor) on Windows. As these seem to be new products, the versions of
JDK that can be installed are limited.

## Java Versions

Java version numbers seem to be all over the place between different vendors
and "modern" (9+) and "legacy" (8 and below) versions of Java. To attempt to
bring some consistency to Java version specification for this role, currently
the `java_version` is expected to be specified with periods between all of the
different Java version numbers (without letters).

This is essentially starting with the official Oracle
[version string format](https://docs.oracle.com/en/java/javase/11/install/version-string-format.html)
and adding an additional part on the end for the vendors who are specifying
yet another number. Basically:

    $FEATURE.$INTERIM.$UPDATE.$PATCH.$BUILD

This means that some of the version numbers you see in the installer names and
documentation may need to be adjusted to be used with this role. This also
includes modifying "legacy" version numbers to match the newer standard.
Examples:

    11.0.2.9.1       ->  11.0.2.9.1
    11.0.2.7-2       ->  11.0.2.7-2
    1.8.0.201-2.b09  ->  8.201-2.09
    8.202.08.2       ->  8.202.08.2

This version number strategy will continue to be evaluated and modified, if
necessary, to accomodate other vendors and versioning schemes as the role is
improved.

## Environment Variables

Variables that are particular to the environment from which you are running
the playbook can be supplied as environment variables so that they can be
"sourced" from a file in the environment.  This provides an easy way to
supply different paths to resources if you are using the roles on different
computers.

| Option                               | Default | Example                                 |
| :----------------------------------- | :------ | :-------------------------------------- |
| `JAVA_LINUX_LOCAL_INSTALLERS_PATH`   | none    | `/Users/Shared/Installers/Linux/Java`   |
| `JAVA_MAC_LOCAL_INSTALLERS_PATH`     | none    | `/Users/Shared/Installers/macOS/Java`   |
| `JAVA_WINDOWS_LOCAL_INSTALLERS_PATH` | none    | `/Users/Shared/Installers/Windows/Java` |
| `LINUX_LOCAL_INSTALLERS_PATH`        | none    | `/Users/Shared/Installers/Linux`        |
| `MAC_LOCAL_INSTALLERS_PATH`          | none    | `/Users/Shared/Installers/macOS`        |
| `WINDOWS_LOCAL_INSTALLERS_PATH`      | none    | `/Users/Shared/Installers/Windows`      |
| `JAVA_LOCAL_INSTALLERS_PATH`         | none    | `/Users/Shared/Installers/Java`         |
| `LOCAL_INSTALLERS_PATH`              | none    | `/Users/Shared/Installers`              |

_Note: One or more of the `INSTALLERS_PATH` environment variables may be_
_defined and the role will search the paths in the above order until it_
_finds an installer. If it does not find an installer locally, it will_
_attempt to download the installer, but this is only likely to work for_
_the latest installer versions, due to download restrictions that Oracle_
_has in place._

Other variables may also be specified with environment variables to make it
easier to specify them on the command line immediately preceding the
ansible-playbook command.

| Option                    | Default | Example                                 |
| :------------------------ | :------ | :-------------------------------------- |
| `JAVA_VERSION`            | none    | `11.0.2.9.1` or `8.202.08.2`            |
| `JAVA_VENDOR`             | none    | `amazon` or `redhat`                    |
| `JAVA_INSTALLER_URL_PATH` | none    | `https://d2znqt9b1bc64u.cloudfront.net` |

## Role Variables

Variables that are targeted toward options to use during the execution of the
roles are left to be specified as role variables and can be specified in the
playbook itself or on the command line when running the playbook.

| Option                      | Default                                 | Example                                                 |
| :-------------------------- | :-------------------------------------- | :------------------------------------------------------ |
| `java_version`              | `11.0.2.9.1`                            | `11.0.2.9.1` or `8.202.08.2`                            |
| `java_vendor`               | `amazon`                                | `amazon` or `redhat`                                    |
| `java_installers_path_list` | [`/Users/Shared/Installers`]            | [`/Users/Shared/Installers`,`/Users/myaccount/Desktop`] |
| `java_installer_url_path`   | `https://d2znqt9b1bc64u.cloudfront.net` | `https://d2znqt9b1bc64u.cloudfront.net`                 |

_Note: Using `java_installers_path_list` or `java_installer_url_path` might_
_not be considered "normal usage", but is supported for use in playbooks or_
_other scenarios in which it makes sense._

## Role Use

Use of this role consists of the following:

- Create a playbook
- Obtain and have the desired installer available locally on the ansible
  controller (or let the role attempt to download the installer)
- Provide the location of the installer on the controller as an environment
  variable, in the playbook or as an extra-var
- Provide the version of Java (see below for more Java version information)
  as an environment variable, in the playbook or as an extra-var
- Run the playbook

### Example Playbooks

``` yaml
- name: Install JDK
    hosts: servers
    roles:
        - { role: kaos2oak.java }
```

_Note: See the `defaults.yml` file for the "default" Java version that will_
_be installed by the above playbook._

``` yaml
- name: Install Amazon Corretto JDK 11.0.2
    hosts: servers
    vars:
        java_version: '11.0.2.9.1'
        java_vendor: 'amazon'
    roles:
        - { role: kaos2oak.java }
```

``` yaml
- name: Install Amazon Corretto JDK 8.202.08.2
    hosts: servers
    vars:
        java_version: '8.202.08.2'
        java_vendor: 'amazon'
    roles:
        - { role: kaos2oak.java }
```

``` yaml
- name: Install RedHat JDK 8.201-2.09 (a.k.a. 1.8.0.201-2.b09)
    hosts: servers
    vars:
        java_version: '8.201-2.09'
        java_vendor: 'redhat'
    roles:
        - { role: kaos2oak.java }
```

### Example Installer Locations

If you really want it to be quick and easy:

    export LOCAL_INSTALLERS_PATH="$HOME/Downloads"

Or, you could always move the installers to a more permanent default location
after downloading them and then point to that location:

    export JAVA_LOCAL_INSTALLERS_PATH="/Users/Shared/Installers/Java"

If you like to keep things neat and organized, you might organize the installers
into folders, create a file named something like `setup` in a directory named
`my` in this repository (most contents of the `my` directory are part of the
.gitignore ignored files, so it will not be part of any commit) and then
`source` the file:

``` shell
# File: setup
export JAVA_MAC_LOCAL_INSTALLERS_PATH="$HOME/Installers/Mac/Java"
export JAVA_LINUX_LOCAL_INSTALLERS_PATH="$HOME/Installers/Linux/Java"
export JAVA_WINDOWS_LOCAL_INSTALLERS_PATH="$HOME/Installers/Windows/Java"
```

    source my/setup

### Example Java Version

Since the Java version and vendor may be something that you want to change on
the fly, you probably don't want to include them in the `setup` file, but you
can always provide them on the command line before the ansible-playbook run:

    export JAVA_VENDOR=redhat JAVA_VERSION=8.201-2.09

Or, provide them as "extra-vars" role variables for the ansible-playbook run:

    -e "java_vendor=redhat java_version=11.0.2.7-2"

### Example Playbook Runs

Assuming you have created a playbook named `k2o-java.yml`:

    ansible-playbook k2o-java.yml

    JAVA_VENDOR=redhat JAVA_VERSION=11.0.2.7-2 ansible-playbook k2o-java.yml

    ansible-playbook k2o-java.yml -e "java_vendor=redhat java_version=11.0.2.7-2"

If the playbook itself contains the version of Java, it might look like:

    ansible-playbook k2o-java-11.0.2.yml

## Role Testing

### Pre-requisites

[Molecule](https://molecule.readthedocs.io/en/latest/) is being used for
testing this role.

_Note: Windows testing with Molecule is not actively supported, so testing for_
_Windows has been omitted._

You will need to install molecule and python support modules before running
the role tests:

    pip install molecule
    pip install docker-py

You also need to install the following before running the vagrant role tests:

    pip install python-vagrant

### Java Versions in Molecule tests

To run the molecule tests for a particular Java version, you will need to
provide the `JAVA_VERSION` as an environment variable and ensure the installer
is located locally in the appropriate ...`INSTALLERS_PATH` location, if
necessary. See examples, below.

It is also possible to edit the `molecule.yml` file for a scenario and
specify the java_version like this:

    provisioner:
      name: ansible
      env:
        JAVA_VERSION: 8.202.08.2

### macOS Tests

macOS 10.13, 10.12, 10.11 via vagrant:

    molecule test --scenario-name macos-vagrant

## License

MIT

## Author Information

Justin Sako