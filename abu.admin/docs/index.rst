.. abu.admin documentation master file, created by
   sphinx-quickstart on Mon May 21 12:10:20 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to abu.admin's documentation!
=====================================

简介
----

abu.admin_ 致力于简化 Python_ 编写的应用程序部署，特别是需要在同一台物理机器上部署多个项目运行环境的情况下尤其有用。它提供简洁的命令行接口方便用户使用。理论上来说，任务项目都可以使用 abu.admin_ 进行部署，只要该项目实现 abu.admin_ 的接口协议。

abu.admin_ 受到 TracAdmin_ 的启发，在此表示感谢。

安装
----

abu.admin_ 已经发布到 pypi_ ，所以通过执行 easy_install/pip 即可完成安装 ``easy_install -U abu.admin`` ，安装时，可能需要超级用户权限或者指定 -i 参数。


初体验
-------

安装完成以后，就可以简单地执行 ``abu.admin`` 来跟它亲密接触一下了。

::

    # abu.admin
    run "abu.admin help" for usage.

abu.admin_ 采用了类似 subversion_ 风格的命令行接口，可以运行多个子命令。

::

    # abu.admin help
    abu.admin <subcommand> [options] [args]
    run "abu.admin help <subcommand>" for usage of subcommand.
    available subcommands:
        init
        backup
        list
        upgrade
        help

从使用帮助可以看到，abu.admin_ 基本用法就是子命令及其参数。目前可用的子命令有：``list``/``init``/``backup``/``upgrade``/``help`` 等。对于子命令的使用，可以执行 ``abu.admin help <subcommand>`` 获得帮助。

::

    # abu.admin help list
    list all applications supported abu.abmin.
    abu.admin list

从上面的执行结果可知 ``list`` 子命令的作用是列出所有支持 abu.admin_ 的应用，其使用方法是 ``abu.admin list`` 。

::

    # abu.admin list
    1 : read_and_display

可以看到当前已经安装了一个支持 abu.admin_ 的应用，名字叫 ``read_and_display`` ，实际上，它是开发 abu.admin_ 时用来测试项目，可以通过源代码安装。

read_and_display 简介
---------------------------------

read_and_display 是作为 abu.admin_ 的示例项目而专门编写的。它的业务逻辑很简单：读取运行目录下的 ``README`` 文件，然后将其内容打印到标准输出。

read_and_display 的代码可以通过 ``svn`` 获取到：

::

    # svn co http://abu-admin.googlecode.com/svn/trunk/abu.admin/test/read_and_display
    # cd read_and_display
    # python setup.py install

执行上述命令后，再运行 ``abu.admin list`` 应该可以看到跟前文一致的输出了。

配置 read_and_display 的运行环境
-----------------------------------------

前文说过，read_and_display 的业务逻辑很简单：读取运行目录下的 ``README`` 文件，然后将其内容打印到标准输出。那么让我们先建立一个目录叫 read_and_display_env  的目录，并在其中运行一下 ``read_and_display`` ：

::

    # cd ~
    # mkdir read_and_display_env
    # cd read_and_display_env/
    # read_and_display
    Traceback (most recent call last):
      File "/usr/local/bin/read_and_display", line 9, in <module>
        load_entry_point('read-and-display==0.1.0dev-r0', 'console_scripts', 'read_and_display')()
      File "/.../abu-admin/abu.admin/test/read_and_display/read_and_display/main.py", line 4, in main
        with open('README') as f:
    IOError: [Errno 2] No such file or directory: 'README'

果然出现了找不到文件的错误。这时候用 abu.admin_ 来初始化一个它的运行环境吧。

::

    # abu.admin init read_and_display .
    # ls
    __ABU_ADMIN_RC___  README

可以看到，本来空无一物的 ``read_and_display_env`` 目录下出现了两个文件，其中一个名字正是叫做 ``README`` ！这时候再来运行一下 ``read_and_display`` 看看：

:: 

    # read_and_display
    read_and_display README

    this is a abu.admin sample project.

哇唔！ ``read_and_display`` 成功运行了！那么 ``read_and_display`` 又是怎么实现对 abu.admin_ 的支持的呢？且听下文分解。

支持 abu.admin_
-------------------------

接口
~~~~~

要支持 abu.admin_ 实际上只需要实现 abu.admin.Interface 类声明的几个接口即可，其接口如下：

::

    class Interface(object):
        def version(self):
            raise NotImplementedError

        def init(self, path):
            raise NotImplementedError

        def backup(self, path, backup_path):
            raise NotImplementedError

        def upgrade(self, path, old_version):
            raise NotImplementedError


实现
~~~~~

在 ``read_and_display`` 项目中，我们实现了 ``version`` 和 ``init`` 两个接口：

::

    import os
    import pkg_resources

    from abu.admin import Interface

    class Admin(Interface):
        def version(self):
            return '0.0.1'
                    
        def init(self, path):
            with open(os.path.join(path, 'README'), 'w') as readme:
                readme.write(pkg_resources.resource_string('read_and_display',
                    'config_templates/README.template'))


可以看到，在 ``init`` 中把 ``config_templates/README.template`` 的内容写入到了指定的路径下的 ``README`` 文件中，完成了初始化运行环境的目标。

与 abu.admin_ 连接
~~~~~~~~~~~~~~~~~~~~~~~

那么，abu.admin_ 又是怎么找到 ``read_and_display`` 项目中的 ``class Admin`` 的呢？答案就是 setuptools_ 的 entry point 机制。打开 ``read_and_display`` 项目的 ``setup.py`` 文件，可以看到以下代码：

::

    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    read_and_display = read_and_display.main:main
    [abu.admin]
    read_and_display = read_and_display.admin:Admin
    """,

其中 ``abu.admin`` 这一节里通过 ``read_and_display = read_and_display.admin:Admin`` 把 ``class Admin`` 作为一个 entry point 告知了 abu.admin_ 并为其所用。

.. _Python: http://www.python.org
.. _pypi: http://pypi.python.org/pypi/abu.admin 
.. _abu.admin: http://code.google.com/abu-admin
.. _TracAdmin: http://trac.edgewall.org/wiki/TracAdmin
.. _subversion: http://subversion.tigris.org/

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

