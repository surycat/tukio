"""
Any data received by the engine is wrapped into an event and passed to
workflows and tasks.
"""
from copy import copy


class EventSource:

    def __init__(self, workflow_template_id=None, workflow_exec_id=None,
                 task_template_id=None, task_exec_id=None):
        self._workflow_template_id = workflow_template_id
        self._workflow_exec_id = workflow_exec_id
        self._task_template_id = task_template_id
        self._task_exec_id = task_exec_id

    def __repr__(self):
        return '<EventSource wflow_template_id={}, wflow_exec_id={}{}>'.format(
            self._workflow_template_id,
            self._workflow_exec_id,
            ', task_template_id={}, task_exec_id={}'.format(
                self._task_template_id, self._task_exec_id
            ) if self._task_template_id and self._task_exec_id else ''
        )

    def __copy__(self):
        return EventSource(
            self._workflow_template_id,
            self._workflow_exec_id,
            self._task_template_id,
            self._task_exec_id
        )

    def as_dict(self):
        return {
            'workflow_template_id': self._workflow_template_id,
            'workflow_exec_id': self._workflow_exec_id,
            'task_template_id': self._task_template_id,
            'task_exec_id': self._task_exec_id
        }


class Event:

    def __init__(self, data, topic=None, source=None):
        """
        Automatically copy the given data and source if any.
        """
        if topic and not isinstance(topic, str):
            raise ValueError('topic must be a string')
        if source and not isinstance(source, EventSource):
            raise ValueError('source must be an EventSource')
        if isinstance(data, dict):
            self._data = copy(data)
        elif isinstance(data, Event):
            self._data = copy(data.data)
        else:
            raise ValueError('data must be a dict or Event')
        self._topic = topic
        self._source = copy(source)

    @property
    def data(self):
        return self._data

    @property
    def topic(self):
        return self._topic

    @property
    def source(self):
        return self._source

    def __str__(self):
        return '<Event data={}, topic={}, source={}>'.format(
            self._data, self._topic, self._source
        )

    def __repr__(self):
        """
        Return a string repr of the data.
        """
        return str(self._data)

    def __copy__(self):
        """
        Return a copy of the event's data.
        """
        return copy(self._data)
