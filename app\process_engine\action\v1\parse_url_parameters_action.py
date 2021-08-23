from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result

import urllib
from urllib.parse import urlparse

class ParseURLParameters(ActionRunner):

    def __init__(self, *args, **kwargs):
        pass

    async def run(self, void):
        try:
            if not isinstance(self.session.context, dict):
                raise KeyError("No session context defined.")

            page_url = self.session.context['page']['url']

            parsed = urlparse(page_url)
            params = urllib.parse.parse_qsl(parsed.query)

            for x, y in params:
                response = {"Parameter": x,
                            "Value": y}

        return Result(port="payload", value=response)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='app.process_engine.action.v1.parse_url_parameters_action',
            className='ParseURLParameters',
            inputs=['void'],
            outputs=['payload'],
        ),
        metadata=MetaData(
            name='Parse URL parameters',
            desc='Reads URL parameters form context, parses it and returns as dictionary.',
            type='flowNode',
            width=100,
            height=100,
            icon='json',
            group=["Read"]
        )
    )
