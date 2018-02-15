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
        task_vars = result._task.get_variable_manager().get_vars(host=result._host, task=result._task, play=result._task._parent._play)
        task_args = result._task.args
        stateful_config = task_vars.get('ansible_stateful_config', [])
        if isinstance(stateful_config, dict):
            stateful_config = [stateful_config]
        for config in stateful_config:
            for capture in config['capture']:
                if result._task.action == capture['action']:
                    field_from = capture.get('from', 'args')
                    value = None
                    if field_from == 'args':
                        if capture['field'] in task_args:
                            value = task_args[capture['field']]
                    elif field_from == 'result':
                        if capture['field'] in result._result:
                            value = result._result[capture['field']]
                    if value:
                        if not config['var_name'] in result._host.vars:
                            result._host.vars[config['var_name']] = []
                        result._host.vars[config['var_name']].append(value)
