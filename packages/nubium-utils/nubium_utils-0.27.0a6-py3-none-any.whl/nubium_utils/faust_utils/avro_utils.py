import json

from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers import FaustSerializer
from .faust_runtime_vars import env_vars
import logging

LOGGER = logging.getLogger(__name__)

def get_avro_client() -> SchemaRegistryClient:
    """
    Configures a client for the schema registry using an environment variable
    :return: (SchemaRegistryClient)
    """
    if env_vars()['SCHEMA_REGISTRY_USERNAME']:
        LOGGER.info('Using RHOSAK schema registry')
        conf = env_vars()["SCHEMA_REGISTRY_SERVER"]
    else:
        LOGGER.info('Using Bifrost schema registry')
        conf = {
            "url": env_vars()["SCHEMA_REGISTRY_SERVER"],
            "ssl.ca.location": env_vars()['SCHEMA_REGISTRY_SSL_CA_LOCATION']
        }
    return SchemaRegistryClient(conf)


def key_serializer(client) -> FaustSerializer:
    """
    Creates Faust Serializer for generic string schema
    """
    return FaustSerializer(schema_registry_client=client,
                           schema_subject='generic_faust_avro_key',
                           schema=schema.AvroSchema('''{"type":"string"}'''))


def value_serializer(client, topic, schema_dict):
    return FaustSerializer(schema_registry_client=client,
                           schema_subject=topic,
                           schema=schema.AvroSchema(json.dumps(schema_dict)))
