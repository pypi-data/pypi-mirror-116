==================
主界面及应用说明
==================

.. sectionauthor:: 侯展意

重要补充说明
-------------------

.. sectionauthor:: 郑君

``Workspace`` 需要用到 ``DataServer``，目前采用 ``FastAPI`` 框架。
但无论什么框架，均引用 ``signal`` 模块，该模块只能在 ``main thread`` 使用。
因此，主线程上必须运行 ``DataServer``，我在 ``pmappmoderm`` 中把 ``GUI`` 移动到新的线程中，``QT`` 会报 ``warning``，但是不影响运行。
如有问题及时联系我。


主界面代码说明
-------------------

源码位置及继承关系
^^^^^^^^^^^^^^^^^^^^^^^^^

主界面类指定义在 ``pmappmodern.py`` 的 ``MainWindow`` 类。


继承自 ``features.ui.generalwidgets.BaseMainWindow`` 。

界面功能
^^^^^^^^^^^^

1. 具有若干可自由拖动的停靠窗口，并可以记忆窗口的布局。
#. 具有若干可通过选项卡切换的工具栏。

工具栏
^^^^^^^^^

添加工具栏
""""""""""""""

主界面的工具栏使用的是 ``PMGToolBar`` 这个类，继承自 ``QToolBar`` 。

主窗口 ``add_tool_bar()`` 方法，可以将 ``QToolBar`` 或 ``PMGToolBar`` ，抑或是你自己的继承于 ``QToolBar`` 的工具栏添加到主窗口。

获取工具栏
""""""""""""""

工具栏通过它的名称进行访问。

预定义的工具栏只有一个,名曰 ``'toolbar_home'`` 。

举个例子讲，要获取主页对应的工具栏，那么就使用 ``MainWindow.toolbars.get('toolbar_home')`` 进行获取就可以了。

在工具栏上添加按钮
"""""""""""""""""""""""""""

获取工具栏后，调用 ``MainWindow.add_tool_button()`` 即可添加一个按钮，或者调用 ``add_tool_buttons()`` 添加多个竖排的按钮。
这两个函数的返回值分别为 ``QPushButton`` 和 ``List[QPushButton]`` 。

在工具栏上添加控件
"""""""""""""""""""""""""""""

添加控件的方法与在 ``QToolBar`` 上添加控件完全相同，亦即继承了 ``addWidget`` 方法，在此不再赘述。

添加带有菜单的按钮
""""""""""""""""""""""""""""

如果需要菜单效果，可以用 ``QMenu`` 写一个菜单，然后添加到按钮之上。

工具栏实现细节
"""""""""""""""""""""""""""

工具栏看似使用了选项卡，其实不然。

最顶端的“选项卡样控件”实为插入了按钮的 ``QToolBar`` ,可以依靠其按钮的点击来进行工具栏的切换。

切换工具栏时，其他工具栏隐藏，只有按钮对应的工具栏可以显示。详见switch_toolbar方法。

主界面停靠窗口
^^^^^^^^^^^^^^^^^^

主界面由一系列 ``PMDockWidget`` 组成。
此控件继承于 ``QDockWidget`` 。

添加停靠窗口的方法
""""""""""""""""""""""""""""

``MainWindow.add_widget_on_dock()`` 方法可以用来将任意控件添加到dock,而且下次加载之时布局会被保存。

停靠窗口的获取
""""""""""""""""""""

``MainWindow.get_dock_widget(widget_name:str)->PMDockWidget``

根据名称进行停靠窗口的获取。如果名称不存在，那么就会抛出异常。

关于快速启动的说明
"""""""""""""""""""""""""""""

为了加快软件启动速度，控件（假设其类名为 ``Widget`` ）可以定义方法 ``Widget.setup_ui`` 。

当加载时，首先执行控件的 ``__init__`` ,并且将 ``setup_ui`` 压入任务栈之中，
等到主界面显示出来之后再用定时器调用执行控件的 ``setup_ui`` 方法。

对于核心控件可以定义 ``show_directly=True`` ，保证立即执行 ``setup_ui`` 方法。
或者干脆不写``setup_ui`` 方法，而是将启动方法放在 ``__init__`` 之中。

窗口隐藏与销毁
""""""""""""""""

``dockwidget`` 的隐藏与显示可以通过主页选项卡中’视图‘菜单进行管理。
当点击窗口关闭按钮的时候，窗口会被“关闭”。
但实际上窗口并未被销毁，也就是被隐藏起来了。
如果确实要销毁窗口，那么请重写 ``PMDockWidget`` 中的 ``closeEvent`` 方法，确保窗口在被关闭的时候被正确销毁了。

对于工具栏基类的建议
""""""""""""""""""""""""""

无论是主界面还是插件，建议继承 ``PMGToolBar`` 类，这个类有设置好的样式。

使用 ``QToolbar`` 尽管不会出错，但是样式很难统一。

.. code-block:: python

    from pmgwidgets import PMGToolBar


主界面的全局获取方法
-------------------------

在 ``pyminer.globals`` 中定义了关于主界面的一些全局操作。


获取主界面
^^^^^^^^^^^^^^^^

.. code-block:: python

    get_main_window()->MainWindow

主界面是一个全局变量，应用启动时对其赋值。
这种写法尽管原始，但主要目的在于尽可能的减少循环导入的可能性，方便未来的插件开发。

获取根路径
^^^^^^^^^^^^^^^^^

.. code-block:: python

    get_root_path()->str



.. toctree::
   :maxdepth: 2

   config/index.rst
   data_adapter/index.rst
   extensions/index.rst
   features/index.rst
   tests/index.rst
   ui/index.rst
   workspace/index.rst
   workspace2/index.rst

   pmappmodern.rst
   globals.rst

