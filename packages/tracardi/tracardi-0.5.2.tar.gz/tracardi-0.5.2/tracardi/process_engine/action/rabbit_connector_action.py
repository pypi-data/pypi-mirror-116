from pydantic import BaseModel
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner

from tracardi.domain.source import Source

class RabbitConfiguration(BaseModel):
    uri: str = 'amqp://guest:guest@127.0.0.1:5672//'

class RabbitPublisherAction(ActionRunner):

    def __init__(self, *args, **kwargs):
        if 'source' not in kwargs:
            raise ValueError('Source not defined.')

        if 'id' not in kwargs['source'] or  kwargs['source']['id'] is None:
            raise ValueError('Source id not defined.')

        self.source_id = kwargs['source']['id']

        source = Source(id=self.source_id, type="queue_config", origin="event")
        self.source = source.storage().load()

        if self.source is None:
            raise ValueError('Source id {} does not exist.'.format(self.source_id))

    async def run(self, void):
        print("end input", void)
        return None


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='app.process_engine.action.v1.rabbit_publisher_action',
            className='RabbitPublisherAction',
            inputs=["payload"],
            outputs=[],
            version='0.1',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "source": {
                    "id": None
                }
            }

        ),
        metadata=MetaData(
            name='Rabbit publisher',
            desc='Publishes payload to rabbitmq.',
            type='flowNode',
            width=200,
            height=100,
            icon='stop',
            group=["Connectors"]
        )
    )
