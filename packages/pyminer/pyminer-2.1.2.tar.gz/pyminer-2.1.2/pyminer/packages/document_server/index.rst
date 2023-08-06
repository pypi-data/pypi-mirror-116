==============================================================================
帮助文档服务器
==============================================================================

.. toctree::
   :maxdepth: 2

   docserver/index.rst

   main.rst

.. automodule:: packages.document_server
    :members:
    :undoc-members:


启动一个基于flask的帮助文档服务器。

目前仅提供一个接口：传入一个函数，打开相应的帮助文档。

以下为一个示例：

.. code-block:: python

    Interface.open_by_function_object(cross)

该函数不会产生任何输出，但是将在帮助浏览器中打开一个文档。
目前没有做任何用户输入检测，在无法打开的情况下，
行为未知。