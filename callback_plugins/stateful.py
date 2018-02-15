from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    # This is meaningless, but it feels right
    CALLBACK_TYPE = 'magic'
    CALLBACK_NAME = 'stateful'
    # Start using this callback plugin as soon as it's loaded
    CALLBACK_NEEDS_WHITELIST = False


    def v2_runner_on_ok(self, result):
        if result._task.action == 'file':
            if not 'file_paths' in result._host.vars:
                result._host.vars['file_paths'] = []
            result._host.vars['file_paths'].append(result._result['dest'])
