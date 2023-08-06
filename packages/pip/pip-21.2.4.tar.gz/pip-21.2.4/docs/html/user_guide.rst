==========
User Guide
==========


Running pip
===========

pip is a command line program. When you install pip, a ``pip`` command is added
to your system, which can be run from the command prompt as follows:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip <pip arguments>

   ``python -m pip`` executes pip using the Python interpreter you
   specified as python. So ``/usr/bin/python3.7 -m pip`` means
   you are executing pip for your interpreter located at /usr/bin/python3.7.

.. tab:: Windows

   .. code-block:: shell

      py -m pip <pip arguments>

   ``py -m pip`` executes pip using the latest Python interpreter you
   have installed. For more details, read the `Python Windows launcher`_ docs.


Installing Packages
===================

pip supports installing from `PyPI`_, version control, local projects, and
directly from distribution files.


The most common scenario is to install from `PyPI`_ using :ref:`Requirement
Specifiers`

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install SomePackage            # latest version
      python -m pip install SomePackage==1.0.4     # specific version
      python -m pip install 'SomePackage>=1.0.4'     # minimum version

.. tab:: Windows

   .. code-block:: shell

      py -m pip install SomePackage            # latest version
      py -m pip install SomePackage==1.0.4     # specific version
      py -m pip install 'SomePackage>=1.0.4'   # minimum version

For more information and examples, see the :ref:`pip install` reference.

.. _PyPI: https://pypi.org/


Basic Authentication Credentials
================================

This is now covered in :doc:`topics/authentication`.

netrc Support
-------------

This is now covered in :doc:`topics/authentication`.

Keyring Support
---------------

This is now covered in :doc:`topics/authentication`.

Using a Proxy Server
====================

When installing packages from `PyPI`_, pip requires internet access, which
in many corporate environments requires an outbound HTTP proxy server.

pip can be configured to connect through a proxy server in various ways:

* using the ``--proxy`` command-line option to specify a proxy in the form
  ``[user:passwd@]proxy.server:port``
* using ``proxy`` in a :ref:`config-file`
* by setting the standard environment-variables ``http_proxy``, ``https_proxy``
  and ``no_proxy``.
* using the environment variable ``PIP_USER_AGENT_USER_DATA`` to include
  a JSON-encoded string in the user-agent variable used in pip's requests.


.. _`Requirements Files`:


Requirements Files
==================

"Requirements files" are files containing a list of items to be
installed using :ref:`pip install` like so:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install -r requirements.txt

.. tab:: Windows

   .. code-block:: shell

      py -m pip install -r requirements.txt

Details on the format of the files are here: :ref:`Requirements File Format`.

Logically, a Requirements file is just a list of :ref:`pip install` arguments
placed in a file. Note that you should not rely on the items in the file being
installed by pip in any particular order.

In practice, there are 4 common uses of Requirements files:

1. Requirements files are used to hold the result from :ref:`pip freeze` for the
   purpose of achieving :doc:`topics/repeatable-installs`.  In
   this case, your requirement file contains a pinned version of everything that
   was installed when ``pip freeze`` was run.

   .. tab:: Unix/macOS

      .. code-block:: shell

         python -m pip freeze > requirements.txt
         python -m pip install -r requirements.txt

   .. tab:: Windows

      .. code-block:: shell

         py -m pip freeze > requirements.txt
         py -m pip install -r requirements.txt

2. Requirements files are used to force pip to properly resolve dependencies.
   pip 20.2 and earlier `doesn't have true dependency resolution
   <https://github.com/pypa/pip/issues/988>`_, but instead simply uses the first
   specification it finds for a project. E.g. if ``pkg1`` requires
   ``pkg3>=1.0`` and ``pkg2`` requires ``pkg3>=1.0,<=2.0``, and if ``pkg1`` is
   resolved first, pip will only use ``pkg3>=1.0``, and could easily end up
   installing a version of ``pkg3`` that conflicts with the needs of ``pkg2``.
   To solve this problem, you can place ``pkg3>=1.0,<=2.0`` (i.e. the correct
   specification) into your requirements file directly along with the other top
   level requirements. Like so::

     pkg1
     pkg2
     pkg3>=1.0,<=2.0

3. Requirements files are used to force pip to install an alternate version of a
   sub-dependency.  For example, suppose ``ProjectA`` in your requirements file
   requires ``ProjectB``, but the latest version (v1.3) has a bug, you can force
   pip to accept earlier versions like so::

     ProjectA
     ProjectB<1.3

4. Requirements files are used to override a dependency with a local patch that
   lives in version control.  For example, suppose a dependency
   ``SomeDependency`` from PyPI has a bug, and you can't wait for an upstream
   fix.
   You could clone/copy the src, make the fix, and place it in VCS with the tag
   ``sometag``.  You'd reference it in your requirements file with a line like
   so::

     git+https://myvcs.com/some_dependency@sometag#egg=SomeDependency

   If ``SomeDependency`` was previously a top-level requirement in your
   requirements file, then **replace** that line with the new line. If
   ``SomeDependency`` is a sub-dependency, then **add** the new line.


It's important to be clear that pip determines package dependencies using
`install_requires metadata
<https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-dependencies>`_,
not by discovering ``requirements.txt`` files embedded in projects.

See also:

* :ref:`Requirements File Format`
* :ref:`pip freeze`
* `"setup.py vs requirements.txt" (an article by Donald Stufft)
  <https://caremad.io/2013/07/setup-vs-requirement/>`_


.. _`Constraints Files`:


Constraints Files
=================

Constraints files are requirements files that only control which version of a
requirement is installed, not whether it is installed or not. Their syntax and
contents is a subset of :ref:`Requirements Files`, with several kinds of syntax
not allowed: constraints must have a name, they cannot be editable, and they
cannot specify extras. In terms of semantics, there is one key difference:
Including a package in a constraints file does not trigger installation of the
package.

Use a constraints file like so:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install -c constraints.txt

.. tab:: Windows

   .. code-block:: shell

      py -m pip install -c constraints.txt

Constraints files are used for exactly the same reason as requirements files
when you don't know exactly what things you want to install. For instance, say
that the "helloworld" package doesn't work in your environment, so you have a
local patched version. Some things you install depend on "helloworld", and some
don't.

One way to ensure that the patched version is used consistently is to
manually audit the dependencies of everything you install, and if "helloworld"
is present, write a requirements file to use when installing that thing.

Constraints files offer a better way: write a single constraints file for your
organisation and use that everywhere. If the thing being installed requires
"helloworld" to be installed, your fixed version specified in your constraints
file will be used.

Constraints file support was added in pip 7.1. In :ref:`Resolver
changes 2020` we did a fairly comprehensive overhaul, removing several
undocumented and unsupported quirks from the previous implementation,
and stripped constraints files down to being purely a way to specify
global (version) limits for packages.

.. _`Installing from Wheels`:


Installing from Wheels
======================

"Wheel" is a built, archive format that can greatly speed installation compared
to building and installing from source archives. For more information, see the
`Wheel docs <https://wheel.readthedocs.io>`_ , :pep:`427`, and :pep:`425`.

pip prefers Wheels where they are available. To disable this, use the
:ref:`--no-binary <install_--no-binary>` flag for :ref:`pip install`.

If no satisfactory wheels are found, pip will default to finding source
archives.


To install directly from a wheel archive:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install SomePackage-1.0-py2.py3-none-any.whl

.. tab:: Windows

   .. code-block:: shell

      py -m pip install SomePackage-1.0-py2.py3-none-any.whl

To include optional dependencies provided in the ``provides_extras``
metadata in the wheel, you must add quotes around the install target
name:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install './somepackage-1.0-py2.py3-none-any.whl[my-extras]'

.. tab:: Windows

   .. code-block:: shell

      py -m pip install './somepackage-1.0-py2.py3-none-any.whl[my-extras]'

.. note::

    In the future, the ``path[extras]`` syntax may become deprecated. It is
    recommended to use PEP 508 syntax wherever possible.

For the cases where wheels are not available, pip offers :ref:`pip wheel` as a
convenience, to build wheels for all your requirements and dependencies.

:ref:`pip wheel` requires the `wheel package
<https://pypi.org/project/wheel/>`_ to be installed, which provides the
"bdist_wheel" setuptools extension that it uses.

To build wheels for your requirements and all their dependencies to a local
directory:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install wheel
      python -m pip wheel --wheel-dir=/local/wheels -r requirements.txt

.. tab:: Windows

   .. code-block:: shell

      py -m pip install wheel
      py -m pip wheel --wheel-dir=/local/wheels -r requirements.txt

And *then* to install those requirements just using your local directory of
wheels (and not from PyPI):

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install --no-index --find-links=/local/wheels -r requirements.txt

.. tab:: Windows

   .. code-block:: shell

      py -m pip install --no-index --find-links=/local/wheels -r requirements.txt


Uninstalling Packages
=====================

pip is able to uninstall most packages like so:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip uninstall SomePackage

.. tab:: Windows

   .. code-block:: shell

      py -m pip uninstall SomePackage


pip also performs an automatic uninstall of an old version of a package
before upgrading to a newer version.

For more information and examples, see the :ref:`pip uninstall` reference.


Listing Packages
================

To list installed packages:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip list
      docutils (0.9.1)
      Jinja2 (2.6)
      Pygments (1.5)
      Sphinx (1.1.2)

.. tab:: Windows

   .. code-block:: console

      C:\> py -m pip list
      docutils (0.9.1)
      Jinja2 (2.6)
      Pygments (1.5)
      Sphinx (1.1.2)


To list outdated packages, and show the latest version available:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip list --outdated
      docutils (Current: 0.9.1 Latest: 0.10)
      Sphinx (Current: 1.1.2 Latest: 1.1.3)

.. tab:: Windows

   .. code-block:: console

      C:\> py -m pip list --outdated
      docutils (Current: 0.9.1 Latest: 0.10)
      Sphinx (Current: 1.1.2 Latest: 1.1.3)

To show details about an installed package:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip show sphinx
      ---
      Name: Sphinx
      Version: 1.1.3
      Location: /my/env/lib/pythonx.x/site-packages
      Requires: Pygments, Jinja2, docutils

.. tab:: Windows

   .. code-block:: console

      C:\> py -m pip show sphinx
      ---
      Name: Sphinx
      Version: 1.1.3
      Location: /my/env/lib/pythonx.x/site-packages
      Requires: Pygments, Jinja2, docutils

For more information and examples, see the :ref:`pip list` and :ref:`pip show`
reference pages.


Searching for Packages
======================

pip can search `PyPI`_ for packages using the ``pip search``
command:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip search "query"

.. tab:: Windows

   .. code-block:: shell

      py -m pip search "query"

The query will be used to search the names and summaries of all
packages.

For more information and examples, see the :ref:`pip search` reference.

.. _`Configuration`:


Configuration
=============

This is now covered in :doc:`topics/configuration`.

.. _config-file:

Config file
-----------

This is now covered in :doc:`topics/configuration`.

Environment Variables
---------------------

This is now covered in :doc:`topics/configuration`.

.. _config-precedence:

Config Precedence
-----------------

This is now covered in :doc:`topics/configuration`.


Command Completion
==================

pip comes with support for command line completion in bash, zsh and fish.

To setup for bash::

    python -m pip completion --bash >> ~/.profile

To setup for zsh::

    python -m pip completion --zsh >> ~/.zprofile

To setup for fish::

    python -m pip completion --fish > ~/.config/fish/completions/pip.fish

Alternatively, you can use the result of the ``completion`` command directly
with the eval function of your shell, e.g. by adding the following to your
startup file::

    eval "`pip completion --bash`"



.. _`Installing from local packages`:


Installing from local packages
==============================

In some cases, you may want to install from local packages only, with no traffic
to PyPI.

First, download the archives that fulfill your requirements:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip download --destination-directory DIR -r requirements.txt

.. tab:: Windows

   .. code-block:: shell

      py -m pip download --destination-directory DIR -r requirements.txt

Note that ``pip download`` will look in your wheel cache first, before
trying to download from PyPI.  If you've never installed your requirements
before, you won't have a wheel cache for those items.  In that case, if some of
your requirements don't come as wheels from PyPI, and you want wheels, then run
this instead:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip wheel --wheel-dir DIR -r requirements.txt

.. tab:: Windows

   .. code-block:: shell

      py -m pip wheel --wheel-dir DIR -r requirements.txt

Then, to install from local only, you'll be using :ref:`--find-links
<install_--find-links>` and :ref:`--no-index <install_--no-index>` like so:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install --no-index --find-links=DIR -r requirements.txt

.. tab:: Windows

   .. code-block:: shell

      py -m pip install --no-index --find-links=DIR -r requirements.txt


"Only if needed" Recursive Upgrade
==================================

``pip install --upgrade`` now has a ``--upgrade-strategy`` option which
controls how pip handles upgrading of dependencies. There are 2 upgrade
strategies supported:

- ``eager``: upgrades all dependencies regardless of whether they still satisfy
  the new parent requirements
- ``only-if-needed``: upgrades a dependency only if it does not satisfy the new
  parent requirements

The default strategy is ``only-if-needed``. This was changed in pip 10.0 due to
the breaking nature of ``eager`` when upgrading conflicting dependencies.

It is important to note that ``--upgrade`` affects *direct requirements* (e.g.
those specified on the command-line or via a requirements file) while
``--upgrade-strategy`` affects *indirect requirements* (dependencies of direct
requirements).

As an example, say ``SomePackage`` has a dependency, ``SomeDependency``, and
both of them are already installed but are not the latest available versions:

- ``pip install SomePackage``: will not upgrade the existing ``SomePackage`` or
  ``SomeDependency``.
- ``pip install --upgrade SomePackage``: will upgrade ``SomePackage``, but not
  ``SomeDependency`` (unless a minimum requirement is not met).
- ``pip install --upgrade SomePackage --upgrade-strategy=eager``: upgrades both
  ``SomePackage`` and ``SomeDependency``.

As an historic note, an earlier "fix" for getting the ``only-if-needed``
behaviour was:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install --upgrade --no-deps SomePackage
      python -m pip install SomePackage

.. tab:: Windows

   .. code-block:: shell

      py -m pip install --upgrade --no-deps SomePackage
      py -m pip install SomePackage


A proposal for an ``upgrade-all`` command is being considered as a safer
alternative to the behaviour of eager upgrading.


User Installs
=============

With Python 2.6 came the `"user scheme" for installation
<https://docs.python.org/3/install/index.html#alternate-installation-the-user-scheme>`_,
which means that all Python distributions support an alternative install
location that is specific to a user.  The default location for each OS is
explained in the python documentation for the `site.USER_BASE
<https://docs.python.org/3/library/site.html#site.USER_BASE>`_ variable.
This mode of installation can be turned on by specifying the :ref:`--user
<install_--user>` option to ``pip install``.

Moreover, the "user scheme" can be customized by setting the
``PYTHONUSERBASE`` environment variable, which updates the value of
``site.USER_BASE``.

To install "SomePackage" into an environment with site.USER_BASE customized to
'/myappenv', do the following:

.. tab:: Unix/macOS

   .. code-block:: shell

      export PYTHONUSERBASE=/myappenv
      python -m pip install --user SomePackage

.. tab:: Windows

   .. code-block:: shell

      set PYTHONUSERBASE=c:/myappenv
      py -m pip install --user SomePackage

``pip install --user`` follows four rules:

#. When globally installed packages are on the python path, and they *conflict*
   with the installation requirements, they are ignored, and *not*
   uninstalled.
#. When globally installed packages are on the python path, and they *satisfy*
   the installation requirements, pip does nothing, and reports that
   requirement is satisfied (similar to how global packages can satisfy
   requirements when installing packages in a ``--system-site-packages``
   virtualenv).
#. pip will not perform a ``--user`` install in a ``--no-site-packages``
   virtualenv (i.e. the default kind of virtualenv), due to the user site not
   being on the python path.  The installation would be pointless.
#. In a ``--system-site-packages`` virtualenv, pip will not install a package
   that conflicts with a package in the virtualenv site-packages.  The --user
   installation would lack sys.path precedence and be pointless.


To make the rules clearer, here are some examples:

From within a ``--no-site-packages`` virtualenv (i.e. the default kind):

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip install --user SomePackage
      Can not perform a '--user' install. User site-packages are not visible in this virtualenv.

.. tab:: Windows

   .. code-block:: console

      C:\> py -m pip install --user SomePackage
      Can not perform a '--user' install. User site-packages are not visible in this virtualenv.


From within a ``--system-site-packages`` virtualenv where ``SomePackage==0.3``
is already installed in the virtualenv:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip install --user SomePackage==0.4
      Will not install to the user site because it will lack sys.path precedence

.. tab:: Windows

   .. code-block:: console

      C:\> py -m pip install --user SomePackage==0.4
      Will not install to the user site because it will lack sys.path precedence

From within a real python, where ``SomePackage`` is *not* installed globally:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip install --user SomePackage
      [...]
      Successfully installed SomePackage

.. tab:: Windows

   .. code-block:: console

      C:\> py -m pip install --user SomePackage
      [...]
      Successfully installed SomePackage

From within a real python, where ``SomePackage`` *is* installed globally, but
is *not* the latest version:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip install --user SomePackage
      [...]
      Requirement already satisfied (use --upgrade to upgrade)
      $ python -m pip install --user --upgrade SomePackage
      [...]
      Successfully installed SomePackage

.. tab:: Windows

   .. code-block:: console

      C:\> py -m pip install --user SomePackage
      [...]
      Requirement already satisfied (use --upgrade to upgrade)
      C:\> py -m pip install --user --upgrade SomePackage
      [...]
      Successfully installed SomePackage

From within a real python, where ``SomePackage`` *is* installed globally, and
is the latest version:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip install --user SomePackage
      [...]
      Requirement already satisfied (use --upgrade to upgrade)
      $ python -m pip install --user --upgrade SomePackage
      [...]
      Requirement already up-to-date: SomePackage
      # force the install
      $ python -m pip install --user --ignore-installed SomePackage
      [...]
      Successfully installed SomePackage

.. tab:: Windows

   .. code-block:: console

      C:\> py -m pip install --user SomePackage
      [...]
      Requirement already satisfied (use --upgrade to upgrade)
      C:\> py -m pip install --user --upgrade SomePackage
      [...]
      Requirement already up-to-date: SomePackage
      # force the install
      C:\> py -m pip install --user --ignore-installed SomePackage
      [...]
      Successfully installed SomePackage

.. _`Repeatability`:


Ensuring Repeatability
======================

This is now covered in :doc:`../topics/repeatable-installs`.

.. _`Fixing conflicting dependencies`:

Fixing conflicting dependencies
===============================

The purpose of this section of documentation is to provide practical suggestions to
pip users who encounter an error where pip cannot install their
specified packages due to conflicting dependencies (a
``ResolutionImpossible`` error).

This documentation is specific to the new resolver, which is the
default behavior in pip 20.3 and later. If you are using pip 20.2, you
can invoke the new resolver by using the flag
``--use-feature=2020-resolver``.

Understanding your error message
--------------------------------

When you get a ``ResolutionImpossible`` error, you might see something
like this:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install package_coffee==0.44.1 package_tea==4.3.0

.. tab:: Windows

   .. code-block:: shell

      py -m pip install package_coffee==0.44.1 package_tea==4.3.0

::

   Due to conflicting dependencies pip cannot install
   package_coffee and package_tea:
   - package_coffee depends on package_water<3.0.0,>=2.4.2
   - package_tea depends on package_water==2.3.1

In this example, pip cannot install the packages you have requested,
because they each depend on different versions of the same package
(``package_water``):

- ``package_coffee`` version ``0.44.1`` depends on a version of
  ``package_water`` that is less than ``3.0.0`` but greater than or equal to
  ``2.4.2``
- ``package_tea`` version ``4.3.0`` depends on version ``2.3.1`` of
  ``package_water``

Sometimes these messages are straightforward to read, because they use
commonly understood comparison operators to specify the required version
(e.g. ``<`` or ``>``).

However, Python packaging also supports some more complex ways for
specifying package versions (e.g. ``~=`` or ``*``):

+----------+---------------------------------+--------------------------------+
| Operator | Description                     | Example                        |
+==========+=================================+================================+
|  ``>``   | Any version greater than        | ``>3.1``: any version          |
|          | the specified version.          | greater than ``3.1``.          |
+----------+---------------------------------+--------------------------------+
|  ``<``   | Any version less than           | ``<3.1``: any version          |
|          | the specified version.          | less than ``3.1``.             |
+----------+---------------------------------+--------------------------------+
|  ``<=``  | Any version less than or        | ``<=3.1``: any version         |
|          | equal to the specified version. | less than or equal to ``3.1``. |
+----------+---------------------------------+--------------------------------+
|  ``>=``  | Any version greater than or     | ``>=3.1``:                     |
|          | equal to the specified version. | version ``3.1`` and greater.   |
+----------+---------------------------------+--------------------------------+
|  ``==``  | Exactly the specified version.  | ``==3.1``: only ``3.1``.       |
+----------+---------------------------------+--------------------------------+
|  ``!=``  | Any version not equal           | ``!=3.1``: any version         |
|          | to the specified version.       | other than ``3.1``.            |
+----------+---------------------------------+--------------------------------+
|  ``~=``  | Any compatible release.         | ``~=3.1``: version ``3.1``     |
|          | Compatible releases are         | or later, but not              |
|          | releases that are within the    | version ``4.0`` or later.      |
|          | same major or minor version,    | ``~=3.1.2``: version ``3.1.2`` |
|          | assuming the package author     | or later, but not              |
|          | is using semantic versioning.   | version ``3.2.0`` or later.    |
+----------+---------------------------------+--------------------------------+
|  ``*``   | Can be used at the end of       | ``==3.1.*``: any version       |
|          | a version number to represent   | that starts with ``3.1``.      |
|          | *all*,                          | Equivalent to ``~=3.1.0``.     |
+----------+---------------------------------+--------------------------------+

The detailed specification of supported comparison operators can be
found in :pep:`440`.

Possible solutions
------------------

The solution to your error will depend on your individual use case. Here
are some things to try:

1. Audit your top level requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a first step it is useful to audit your project and remove any
unnecessary or out of date requirements (e.g. from your ``setup.py`` or
``requirements.txt`` files). Removing these can significantly reduce the
complexity of your dependency tree, thereby reducing opportunities for
conflicts to occur.

2. Loosen your top level requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes the packages that you have asked pip to install are
incompatible because you have been too strict when you specified the
package version.

In our first example both ``package_coffee`` and ``package_tea`` have been
*pinned* to use specific versions
(``package_coffee==0.44.1b0 package_tea==4.3.0``).

To find a version of both ``package_coffee`` and ``package_tea`` that depend on
the same version of ``package_water``, you might consider:

-  Loosening the range of packages that you are prepared to install
   (e.g. ``pip install "package_coffee>0.44.*" "package_tea>4.0.0"``)
-  Asking pip to install *any* version of ``package_coffee`` and ``package_tea``
   by removing the version specifiers altogether (e.g.
   ``python -m pip install package_coffee package_tea``)

In the second case, pip will automatically find a version of both
``package_coffee`` and ``package_tea`` that depend on the same version of
``package_water``, installing:

-  ``package_coffee 0.46.0b0``, which depends on ``package_water 2.6.1``
-  ``package_tea 4.3.0`` which *also* depends on ``package_water 2.6.1``

If you want to prioritize one package over another, you can add version
specifiers to *only* the more important package:

.. tab:: Unix/macOS

   .. code-block:: shell

      python -m pip install package_coffee==0.44.1b0 package_tea

.. tab:: Windows

   .. code-block:: shell

      py -m pip install package_coffee==0.44.1b0 package_tea

This will result in:

- ``package_coffee 0.44.1b0``, which depends on ``package_water 2.6.1``
- ``package_tea 4.1.3`` which also depends on ``package_water 2.6.1``

Now that you have resolved the issue, you can repin the compatible
package versions as required.

3. Loosen the requirements of your dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming that you cannot resolve the conflict by loosening the version
of the package you require (as above), you can try to fix the issue on
your *dependency* by:

-  Requesting that the package maintainers loosen *their* dependencies
-  Forking the package and loosening the dependencies yourself

.. warning::

   If you choose to fork the package yourself, you are *opting out* of
   any support provided by the package maintainers. Proceed at your own risk!

4. All requirements are loose, but a solution does not exist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes it's simply impossible to find a combination of package
versions that do not conflict. Welcome to `dependency hell`_.

In this situation, you could consider:

-  Using an alternative package, if that is acceptable for your project.
   See `Awesome Python`_ for similar packages.
-  Refactoring your project to reduce the number of dependencies (for
   example, by breaking up a monolithic code base into smaller pieces)

.. _`Getting help`:

Getting help
------------

If none of the suggestions above work for you, we recommend that you ask
for help on:

-  `Python user Discourse`_
-  `Python user forums`_
-  `Python developers Slack channel`_
-  `Python IRC`_
-  `Stack Overflow`_

See `"How do I ask a good question?"`_ for tips on asking for help.

Unfortunately, **the pip team cannot provide support for individual
dependency conflict errors**. Please *only* open a ticket on the `pip
issue tracker`_ if you believe that your problem has exposed a bug in pip.

.. _dependency hell: https://en.wikipedia.org/wiki/Dependency_hell
.. _Awesome Python: https://python.libhunt.com/
.. _Python user Discourse: https://discuss.python.org/c/users/7
.. _Python user forums: https://www.python.org/community/forums/
.. _Python developers Slack channel: https://pythondev.slack.com/
.. _Python IRC: https://www.python.org/community/irc/
.. _Stack Overflow: https://stackoverflow.com/questions/tagged/python
.. _"How do I ask a good question?": https://stackoverflow.com/help/how-to-ask
.. _pip issue tracker: https://github.com/pypa/pip/issues

.. _`Dependency resolution backtracking`:

Dependency resolution backtracking
==================================

Or more commonly known as *"Why does pip download multiple versions of
the same package over and over again during an install?"*.

The purpose of this section is to provide explanation of why
backtracking happens, and practical suggestions to pip users who
encounter it during a ``pip install``.

What is backtracking?
---------------------

Backtracking is not a bug, or an unexpected behaviour. It is part of the
way pip's dependency resolution process works.

During a pip install (e.g. ``pip install tea``), pip needs to work out
the package's dependencies (e.g. ``spoon``, ``hot-water``, ``cup`` etc.), the
versions of each of these packages it needs to install. For each package
pip needs to decide which version is a good candidate to install.

A "good candidate" means a version of each package that is compatible with all
the other package versions being installed at the same time.

In the case where a package has a lot of versions, arriving at a good
candidate can take a lot of time. (The amount of time depends on the
package size, the number of versions pip must try, and other concerns.)

How does backtracking work?
^^^^^^^^^^^^^^^^^^^^^^^^^^^

When doing a pip install, pip starts by making assumptions about the
packages it needs to install. During the install process it needs to check these
assumptions as it goes along.

When pip finds that an assumption is incorrect, it has to try another approach
(backtrack), which means discarding some of the work that has already been done,
and going back to choose another path.

For example; The user requests ``pip install tea``. ``tea`` has dependencies of
``cup``, ``hot-water``, ``spoon`` amongst others.

pip starts by installing a version of ``cup``. If it finds out it isn’t
compatible (with the other package versions) it needs to “go back”
(backtrack) and download an older version.

It then tries to install that version. If it is successful, it will continue
onto the next package. If not it will continue to backtrack until it finds a
compatible version.

This backtrack behaviour can end in 2 ways - either 1) it will
successfully find a set of packages it can install (good news!), or 2) it will
eventually display a `resolution impossible <https://pip.pypa.io/en/latest/user_guide/#id35>`__ error
message (not so good).

If pip starts backtracking during dependency resolution, it does not
know how long it will backtrack, and how much computation would be
needed. For the user this means it can take a long time to complete.

Why does backtracking occur?
----------------------------

With the release of the new resolver (:ref:`Resolver changes 2020`), pip is now
more strict in the package versions it installs when a user runs a
``pip install`` command.

Pip needs to backtrack because initially, it doesn't have all the information it
needs to work out the correct set of packages. This is because package indexes
don't provide full package dependency information before you have downloaded
the package.

This new resolver behaviour means that pip works harder to find out which
version of a package is a good candidate to install. It reduces the risk that
installing a new package will accidentally break an existing installed package,
and so reduces the risk that your environment gets messed up.

What does this behaviour look like?
-----------------------------------

Right now backtracking behaviour looks like this:

::

   $ pip install tea==1.9.8
   Collecting tea==1.9.8
     Downloading tea-1.9.8-py2.py3-none-any.whl (346 kB)
        |████████████████████████████████| 346 kB 10.4 MB/s
   Collecting spoon==2.27.0
     Downloading spoon-2.27.0-py2.py3-none-any.whl (312 kB)
        |████████████████████████████████| 312 kB 19.2 MB/s
   Collecting hot-water>=0.1.9
   Downloading hot-water-0.1.13-py3-none-any.whl (9.3 kB)
   Collecting cup>=1.6.0
     Downloading cup-3.22.0-py2.py3-none-any.whl (397 kB)
        |████████████████████████████████| 397 kB 28.2 MB/s
   INFO: pip is looking at multiple versions of this package to determine
   which version is compatible with other requirements.
   This could take a while.
     Downloading cup-3.21.0-py2.py3-none-any.whl (395 kB)
        |████████████████████████████████| 395 kB 27.0 MB/s
     Downloading cup-3.20.0-py2.py3-none-any.whl (394 kB)
        |████████████████████████████████| 394 kB 24.4 MB/s
     Downloading cup-3.19.1-py2.py3-none-any.whl (394 kB)
        |████████████████████████████████| 394 kB 21.3 MB/s
     Downloading cup-3.19.0-py2.py3-none-any.whl (394 kB)
        |████████████████████████████████| 394 kB 26.2 MB/s
     Downloading cup-3.18.0-py2.py3-none-any.whl (393 kB)
        |████████████████████████████████| 393 kB 22.1 MB/s
     Downloading cup-3.17.0-py2.py3-none-any.whl (382 kB)
        |████████████████████████████████| 382 kB 23.8 MB/s
     Downloading cup-3.16.0-py2.py3-none-any.whl (376 kB)
        |████████████████████████████████| 376 kB 27.5 MB/s
     Downloading cup-3.15.1-py2.py3-none-any.whl (385 kB)
        |████████████████████████████████| 385 kB 30.4 MB/s
   INFO: pip is looking at multiple versions of this package to determine
   which version is compatible with other requirements.
   This could take a while.
     Downloading cup-3.15.0-py2.py3-none-any.whl (378 kB)
        |████████████████████████████████| 378 kB 21.4 MB/s
     Downloading cup-3.14.0-py2.py3-none-any.whl (372 kB)
        |████████████████████████████████| 372 kB 21.1 MB/s
     Downloading cup-3.13.1-py2.py3-none-any.whl (381 kB)
        |████████████████████████████████| 381 kB 21.8 MB/s
   This is taking longer than usual. You might need to provide the
   dependency resolver with stricter constraints to reduce runtime.
   If you want to abort this run, you can press Ctrl + C to do so.
     Downloading cup-3.13.0-py2.py3-none-any.whl (374 kB)

In the above sample output, pip had to download multiple versions of
package ``cup`` - cup-3.22.0 to cup-3.13.0 - to find a version that will be
compatible with the other packages - ``spoon``, ``hot-water``, etc.

These multiple ``Downloading cup-version`` lines show pip backtracking.

Possible ways to reduce backtracking occurring
----------------------------------------------

It's important to mention backtracking behaviour is expected during a
``pip install`` process. What pip is trying to do is complicated - it is
working through potentially millions of package versions to identify the
compatible versions.

There is no guaranteed solution to backtracking but you can reduce it -
here are a number of ways.

.. _1-allow-pip-to-complete-its-backtracking:

1. Allow pip to complete its backtracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In most cases, pip will complete the backtracking process successfully.
It is possible this could take a very long time to complete - this may
not be your preferred option.

However, there is a possibility pip will not be able to find a set of
compatible versions.

If you'd prefer not to wait, you can interrupt pip (ctrl and c) and use
:ref:`Constraints Files`: to reduce the number of package versions it tries.

.. _2-reduce-the-versions-of-the-backtracking-package:

2. Reduce the number of versions pip will try to backtrack through
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If pip is backtracking more than you'd like, the next option is to
constrain the number of package versions it tries.

A first good candidate for this constraining is the package(s) it is
backtracking on (e.g. in the above example - ``cup``).

You could try:

``pip install tea "cup > 3.13"``

This will reduce the number of versions of ``cup`` it tries, and
possibly reduce the time pip takes to install.

There is a possibility that if you're wrong (in this case an older
version would have worked) then you missed the chance to use it. This
can be trial and error.

.. _3-use-constraint-files-or-lockfiles:

3. Use constraint files or lockfiles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This option is a progression of 2 above. It requires users to know how
to inspect:

-  the packages they're trying to install
-  the package release frequency and compatibility policies
-  their release notes and changelogs from past versions

During deployment, you can create a lockfile stating the exact package and
version number for for each dependency of that package. You can create this
with `pip-tools <https://github.com/jazzband/pip-tools/>`__.

This means the "work" is done once during development process, and so
will save users this work during deployment.

The pip team is not available to provide support in helping you create a
suitable constraints file.

.. _4-be-more-strict-on-package-dependencies-during-development:

4. Be more strict on package dependencies during development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For package maintainers during software development, give pip some help by
creating constraint files for the dependency tree. This will reduce the
number of versions it will try.

Getting help
------------

If none of the suggestions above work for you, we recommend that you ask
for help. :ref:`Getting help`.

.. _`Using pip from your program`:

Using pip from your program
===========================

As noted previously, pip is a command line program. While it is implemented in
Python, and so is available from your Python code via ``import pip``, you must
not use pip's internal APIs in this way. There are a number of reasons for this:

#. The pip code assumes that is in sole control of the global state of the
   program.
   pip manages things like the logging system configuration, or the values of
   the standard IO streams, without considering the possibility that user code
   might be affected.

#. pip's code is *not* thread safe. If you were to run pip in a thread, there
   is no guarantee that either your code or pip's would work as you expect.

#. pip assumes that once it has finished its work, the process will terminate.
   It doesn't need to handle the possibility that other code will continue to
   run after that point, so (for example) calling pip twice in the same process
   is likely to have issues.

This does not mean that the pip developers are opposed in principle to the idea
that pip could be used as a library - it's just that this isn't how it was
written, and it would be a lot of work to redesign the internals for use as a
library, handling all of the above issues, and designing a usable, robust and
stable API that we could guarantee would remain available across multiple
releases of pip. And we simply don't currently have the resources to even
consider such a task.

What this means in practice is that everything inside of pip is considered an
implementation detail. Even the fact that the import name is ``pip`` is subject
to change without notice. While we do try not to break things as much as
possible, all the internal APIs can change at any time, for any reason. It also
means that we generally *won't* fix issues that are a result of using pip in an
unsupported way.

It should also be noted that installing packages into ``sys.path`` in a running
Python process is something that should only be done with care. The import
system caches certain data, and installing new packages while a program is
running may not always behave as expected. In practice, there is rarely an
issue, but it is something to be aware of.

Having said all of the above, it is worth covering the options available if you
decide that you do want to run pip from within your program. The most reliable
approach, and the one that is fully supported, is to run pip in a subprocess.
This is easily done using the standard ``subprocess`` module::

  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])

If you want to process the output further, use one of the other APIs in the module.
We are using `freeze`_ here which outputs installed packages in requirements format.::

  reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])

If you don't want to use pip's command line functionality, but are rather
trying to implement code that works with Python packages, their metadata, or
PyPI, then you should consider other, supported, packages that offer this type
of ability. Some examples that you could consider include:

* ``packaging`` - Utilities to work with standard package metadata (versions,
  requirements, etc.)

* ``setuptools`` (specifically ``pkg_resources``) - Functions for querying what
  packages the user has installed on their system.

* ``distlib`` - Packaging and distribution utilities (including functions for
  interacting with PyPI).

.. _changes-to-the-pip-dependency-resolver-in-20-2-2020:

.. _`Resolver changes 2020`:

Changes to the pip dependency resolver in 20.3 (2020)
=====================================================

pip 20.3 has a new dependency resolver, on by default for Python 3
users. (pip 20.1 and 20.2 included pre-release versions of the new
dependency resolver, hidden behind optional user flags.) Read below
for a migration guide, how to invoke the legacy resolver, and the
deprecation timeline. We also made a `two-minute video explanation`_
you can watch.

We will continue to improve the pip dependency resolver in response to
testers' feedback. Please give us feedback through the `resolver
testing survey`_.

.. _`Migration guide for 2020 resolver changes`:

Watch out for
-------------

The big change in this release is to the pip dependency resolver
within pip.

Computers need to know the right order to install pieces of software
("to install ``x``, you need to install ``y`` first"). So, when Python
programmers share software as packages, they have to precisely describe
those installation prerequisites, and pip needs to navigate tricky
situations where it's getting conflicting instructions. This new
dependency resolver will make pip better at handling that tricky
logic, and make pip easier for you to use and troubleshoot.

The most significant changes to the resolver are:

* It will **reduce inconsistency**: it will *no longer install a
  combination of packages that is mutually inconsistent*. In older
  versions of pip, it is possible for pip to install a package which
  does not satisfy the declared requirements of another installed
  package. For example, in pip 20.0, ``pip install "six<1.12"
  "virtualenv==20.0.2"`` does the wrong thing, “successfully” installing
  ``six==1.11``, even though ``virtualenv==20.0.2`` requires
  ``six>=1.12.0,<2`` (`defined here
  <https://github.com/pypa/virtualenv/blob/20.0.2/setup.cfg#L42-L50>`__).
  The new resolver, instead, outright rejects installing anything if it
  gets that input.

* It will be **stricter** - if you ask pip to install two packages with
  incompatible requirements, it will refuse (rather than installing a
  broken combination, like it did in previous versions).

So, if you have been using workarounds to force pip to deal with
incompatible or inconsistent requirements combinations, now's a good
time to fix the underlying problem in the packages, because pip will
be stricter from here on out.

This also means that, when you run a ``pip install`` command, pip only
considers the packages you are installing in that command, and **may
break already-installed packages**. It will not guarantee that your
environment will be consistent all the time. If you ``pip install x``
and then ``pip install y``, it's possible that the version of ``y``
you get will be different than it would be if you had run ``pip
install x y`` in a single command. We are considering changing this
behavior (per :issue:`7744`) and would like your thoughts on what
pip's behavior should be; please answer `our survey on upgrades that
create conflicts`_.

We are also changing our support for :ref:`Constraints Files`,
editable installs, and related functionality. We did a fairly
comprehensive overhaul and stripped constraints files down to being
purely a way to specify global (version) limits for packages, and so
some combinations that used to be allowed will now cause
errors. Specifically:

* Constraints don't override the existing requirements; they simply
  constrain what versions are visible as input to the resolver (see
  :issue:`9020`)
* Providing an editable requirement (``-e .``) does not cause pip to
  ignore version specifiers or constraints (see :issue:`8076`), and if
  you have a conflict between a pinned requirement and a local
  directory then pip will indicate that it cannot find a version
  satisfying both (see :issue:`8307`)
* Hash-checking mode requires that all requirements are specified as a
  ``==`` match on a version and may not work well in combination with
  constraints (see :issue:`9020` and :issue:`8792`)
* If necessary to satisfy constraints, pip will happily reinstall
  packages, upgrading or downgrading, without needing any additional
  command-line options (see :issue:`8115` and :doc:`development/architecture/upgrade-options`)
* Unnamed requirements are not allowed as constraints (see :issue:`6628` and :issue:`8210`)
* Links are not allowed as constraints (see :issue:`8253`)
* Constraints cannot have extras (see :issue:`6628`)

Per our :ref:`Python 2 Support` policy, pip 20.3 users who are using
Python 2 will use the legacy resolver by default. Python 2 users
should upgrade to Python 3 as soon as possible, since in pip 21.0 in
January 2021, pip dropped support for Python 2 altogether.


How to upgrade and migrate
--------------------------

1. **Install pip 20.3** with ``python -m pip install --upgrade pip``.

2. **Validate your current environment** by running ``pip check``. This
   will report if you have any inconsistencies in your set of installed
   packages. Having a clean installation will make it much less likely
   that you will hit issues with the new resolver (and may
   address hidden problems in your current environment!). If you run
   ``pip check`` and run into stuff you can’t figure out, please `ask
   for help in our issue tracker or chat <https://pip.pypa.io/>`__.

3. **Test the new version of pip**.

   While we have tried to make sure that pip’s test suite covers as
   many cases as we can, we are very aware that there are people using
   pip with many different workflows and build processes, and we will
   not be able to cover all of those without your help.

   -  If you use pip to install your software, try out the new resolver
      and let us know if it works for you with ``pip install``. Try:

      - installing several packages simultaneously
      - re-creating an environment using a ``requirements.txt`` file
      - using ``pip install --force-reinstall`` to check whether
        it does what you think it should
      - using constraints files
      - the "Setups to test with special attention" and "Examples to try" below

   -  If you have a build pipeline that depends on pip installing your
      dependencies for you, check that the new resolver does what you
      need.

   -  Run your project’s CI (test suite, build process, etc.) using the
      new resolver, and let us know of any issues.
   -  If you have encountered resolver issues with pip in the past,
      check whether the new resolver fixes them, and read :ref:`Fixing
      conflicting dependencies`. Also, let us know if the new resolver
      has issues with any workarounds you put in to address the
      current resolver’s limitations. We’ll need to ensure that people
      can transition off such workarounds smoothly.
   -  If you develop or support a tool that wraps pip or uses it to
      deliver part of your functionality, please test your integration
      with pip 20.3.

4. **Troubleshoot and try these workarounds if necessary.**

   -  If pip is taking longer to install packages, read
      :ref:`Dependency resolution backtracking` for ways to reduce the
      time pip spends backtracking due to dependency conflicts.
   -  If you don't want pip to actually resolve dependencies, use the
      ``--no-deps`` option. This is useful when you have a set of package
      versions that work together in reality, even though their metadata says
      that they conflict. For guidance on a long-term fix, read
      :ref:`Fixing conflicting dependencies`.
   -  If you run into resolution errors and need a workaround while you're
      fixing their root causes, you can choose the old resolver behavior using
      the flag ``--use-deprecated=legacy-resolver``. This will work until we
      release pip 21.0 (see
      :ref:`Deprecation timeline for 2020 resolver changes`).

5. **Please report bugs** through the `resolver testing survey`_.


Setups to test with special attention
-------------------------------------

*    Requirements files with 100+ packages

*    Installation workflows that involve multiple requirements files

*    Requirements files that include hashes (:ref:`hash-checking mode`)
     or pinned dependencies (perhaps as output from ``pip-compile`` within
     ``pip-tools``)

*    Using :ref:`Constraints Files`

*    Continuous integration/continuous deployment setups

*    Installing from any kind of version control systems (i.e., Git, Subversion, Mercurial, or CVS), per :doc:`topics/vcs-support`

*    Installing from source code held in local directories

Examples to try
^^^^^^^^^^^^^^^

Install:

* `tensorflow`_
* ``hacking``
* ``pycodestyle``
* ``pandas``
* ``tablib``
* ``elasticsearch`` and ``requests`` together
* ``six`` and ``cherrypy`` together
* ``pip install flake8-import-order==0.17.1 flake8==3.5.0 --use-feature=2020-resolver``
* ``pip install tornado==5.0 sprockets.http==1.5.0 --use-feature=2020-resolver``

Try:

* ``pip install``
* ``pip uninstall``
* ``pip check``
* ``pip cache``


Tell us about
-------------

Specific things we'd love to get feedback on:

*    Cases where the new resolver produces the wrong result,
     obviously. We hope there won't be too many of these, but we'd like
     to trap such bugs before we remove the legacy resolver.

*    Cases where the resolver produced an error when you believe it
     should have been able to work out what to do.

*    Cases where the resolver gives an error because there's a problem
     with your requirements, but you need better information to work out
     what's wrong.

*    If you have workarounds to address issues with the current resolver,
     does the new resolver let you remove those workarounds? Tell us!

Please let us know through the `resolver testing survey`_.

.. _`Deprecation timeline for 2020 resolver changes`:

Deprecation timeline
--------------------

We plan for the resolver changeover to proceed as follows, using
:ref:`Feature Flags` and following our :ref:`Release Cadence`:

*    pip 20.1: an alpha version of the new resolver was available,
     opt-in, using the optional flag
     ``--unstable-feature=resolver``. pip defaulted to legacy
     behavior.

*    pip 20.2: a beta of the new resolver was available, opt-in, using
     the flag ``--use-feature=2020-resolver``. pip defaulted to legacy
     behavior. Users of pip 20.2 who want pip to default to using the
     new resolver can run ``pip config set global.use-feature
     2020-resolver`` (for more on that and the alternate
     ``PIP_USE_FEATURE`` environment variable option, see `issue
     8661`_).

*    pip 20.3: pip defaults to the new resolver in Python 3 environments,
     but a user can opt-out and choose the old resolver behavior,
     using the flag ``--use-deprecated=legacy-resolver``. In Python 2
     environments, pip defaults to the old resolver, and the new one is
     available using the flag ``--use-feature=2020-resolver``.

*    pip 21.0: pip uses new resolver by default, and the old resolver is
     no longer supported. It will be removed after a currently undecided
     amount of time, as the removal is dependent on pip's volunteer
     maintainers' availability. Python 2 support is removed per our
     :ref:`Python 2 Support` policy.

Since this work will not change user-visible behavior described in the
pip documentation, this change is not covered by the :ref:`Deprecation
Policy`.

Context and followup
--------------------

As discussed in `our announcement on the PSF blog`_, the pip team are
in the process of developing a new "dependency resolver" (the part of
pip that works out what to install based on your requirements).

We're tracking our rollout in :issue:`6536` and you can watch for
announcements on the `low-traffic packaging announcements list`_ and
`the official Python blog`_.

.. _freeze: https://pip.pypa.io/en/latest/reference/pip_freeze/
.. _resolver testing survey: https://tools.simplysecure.org/survey/index.php?r=survey/index&sid=989272&lang=en
.. _issue 8661: https://github.com/pypa/pip/issues/8661
.. _our announcement on the PSF blog: http://pyfound.blogspot.com/2020/03/new-pip-resolver-to-roll-out-this-year.html
.. _two-minute video explanation: https://www.youtube.com/watch?v=B4GQCBBsuNU
.. _tensorflow: https://pypi.org/project/tensorflow/
.. _low-traffic packaging announcements list: https://mail.python.org/mailman3/lists/pypi-announce.python.org/
.. _our survey on upgrades that create conflicts: https://docs.google.com/forms/d/e/1FAIpQLSeBkbhuIlSofXqCyhi3kGkLmtrpPOEBwr6iJA6SzHdxWKfqdA/viewform
.. _the official Python blog: https://blog.python.org/
.. _Python Windows launcher: https://docs.python.org/3/using/windows.html#launcher
