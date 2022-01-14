from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.action_runner import ActionRunner
from pydantic import BaseModel, validator
from typing import Dict, Any
from tracardi.service.plugin.domain.result import Result


class Config(BaseModel):
    value: str
    mapping: Dict[str, Any]

    @validator('mapping')
    def validate_mapping(cls, value):
        if not value:
            raise ValueError("Mapping cannot be empty.")
        return value


def validate(config: dict):
    return Config(**config)


class MappingAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = Config(**kwargs)

    async def run(self, payload):
        dot = self._get_dot_accessor(payload)
        self.config.value = dot[self.config.value]

        self.config.mapping = {dot[key]: dot[value] for key, value in self.config.mapping.items()}

        value = self.config.mapping.get(self.config.value, None)

        return Result(port="result", value={"value": value})


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='MappingAction',
            inputs=["payload"],
            outputs=["result"],
            version='0.6.1',
            license="MIT",
            author="Dawid Kruk",
            manual="mapping_action",
            init={
                "value": None,
                "mapping": {}
            },
            form=Form(
                groups=[
                    FormGroup(
                        name="Mapping configuration",
                        fields=[
                            FormField(
                                id="value",
                                name="Value",
                                description="Please provide a path to the value to match.",
                                component=FormComponent(type="dotPath", props={"label": "Prefix"})
                            ),
                            FormField(
                                id="mapping",
                                name="Set of data to match",
                                description="Please provide key-value pairs. Value will be returned if the value"
                                            "is the same as the key from this set.",
                                component=FormComponent(type="keyValueList", props={"label": "List"})
                            )
                        ]
                    )
                ]
            )

        ),
        metadata=MetaData(
            name='Value mapping',
            desc='It returns matching value form the set of data.',
            icon='map-properties',
            group=["Data processing"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "result": PortDoc(desc="This ports returns matched value.")
                }
            )
        )
    )