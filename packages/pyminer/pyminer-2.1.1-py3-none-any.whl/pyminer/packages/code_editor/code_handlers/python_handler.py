from functools import cached_property
from typing import TYPE_CHECKING

from packages.code_editor.code_handlers.base_handler import BaseHandler

if TYPE_CHECKING:
    from packages.ipython_console.main import ConsoleInterface


class PythonHandler(BaseHandler):
    @cached_property
    def ipython_console(self) -> 'ConsoleInterface':
        return self.extension_lib.get_interface('ipython_console')

    def run_code(self, code: str, hint: str = ''):
        if hint == '':
            hint = self.tr('Run code')
        self.ipython_console.run_command(command=code, hint_text=hint, hidden=False)

    def run_selected_code(self):
        code = self.analyzer.selected_code
        self.ipython_console.run_command(command=code, hint_text=code, hidden=False)
