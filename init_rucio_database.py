# -*- coding: utf-8 -*-

# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License"), enclosed in this repository;
# You may not use this file except in compliance with the License.
#
# Based on the work of the Rucio team.
#
# Author:
# - Gabriele Gateano Fronzé, <gfronze@cern.ch>, 2019
#
# PY3K COMPATIBLE

import os
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, event

# os.environ["RUCIO_HOME"]="/opt/rucio-db-init"

from rucio.common.config import config_get
from rucio.db.sqla.models import (SoftModelBase, Account, AccountAttrAssociation, Identity, IdentityAccountAssociation, Scope, DataIdentifier, DidMeta, 
                                    DeletedDataIdentifier, UpdatedDID, BadReplicas, BadPFNs, QuarantinedReplica, DIDKey, DIDKeyValueAssociation, DataIdentifierAssociation, 
                                    ConstituentAssociation, ConstituentAssociationHistory, DataIdentifierAssociationHistory, RSE, RSELimit, RSETransferLimit, RSEUsage, 
                                    UpdatedRSECounter, RSEAttrAssociation, RSEProtocols, AccountLimit, AccountUsage, RSEFileAssociation, CollectionReplica, UpdatedCollectionReplica, RSEFileAssociationHistory, ReplicationRule, ReplicationRuleHistoryRecent, ReplicationRuleHistory, ReplicaLock, DatasetLock, UpdatedAccountCounter, 
                                    Request, Source, Distance, Subscription, Token, Message, MessageHistory, AlembicVersion, Config, Heartbeats, NamingConvention, TemporaryDataIdentifier, LifetimeExceptions)
from rucio.db.sqla.models import register_models
from rucio.db.sqla.session import mysql_ping_listener, mysql_convert_decimal_to_float, psql_convert_decimal_to_float, _fk_pragma_on_connect, my_on_connect

# def get_config_parser(cfg_file_path):
#     """ Reads specified config file in a config parser.
#         :returns: config_parser
#     """

#     config_parser = ConfigParser.SafeConfigParser(os.environ)

#     has_config = config_parser.read(cfg_file_path) == [cfg_file_path]

#     if not has_config:
#         raise Exception('Could not load rucio configuration file rucio.cfg.'
#                         'Rucio looks in the following directories for a configuration file, in order:'
#                         '\n\t${RUCIO_HOME}/etc/rucio.cfg'
#                         '\n\t/opt/rucio/etc/rucio.cfg'
#                         '\n\t${VIRTUAL_ENV}/etc/rucio.cfg')

#     return config_parser

def get_temp_engine(echo=True):
    """ Creates a engine to a specific database.
        :returns: engine
    """

    sql_connection = config_get('database', 'default')
    config_params = [('pool_size', int), ('max_overflow', int), ('pool_timeout', int),
                        ('pool_recycle', int), ('echo', int), ('echo_pool', str),
                        ('pool_reset_on_return', str), ('use_threadlocal', int)]
    params = {}
    for param, param_type in config_params:
        try:
            params[param] = param_type(config_get('database', param))
        except:
            pass
    engine = create_engine(sql_connection, **params)
    if 'mysql' in sql_connection:
        event.listen(engine, 'checkout', mysql_ping_listener)
        event.listen(engine, 'connect', mysql_convert_decimal_to_float)
    elif 'postgresql' in sql_connection:
        event.listen(engine, 'connect', psql_convert_decimal_to_float)
    elif 'sqlite' in sql_connection:
        event.listen(engine, 'connect', _fk_pragma_on_connect)
    elif 'oracle' in sql_connection:
        event.listen(engine, 'connect', my_on_connect)
    assert engine
    return engine

def init_rucio_database(echo=True, tests=False):
    """ Applies the schema to the database. Run this command once to build the database. """

    rucio_cfg_file = os.environ["RUCIO_HOME"]+"/etc/rucio.cfg"
    alembic_cfg_file = os.environ["RUCIO_HOME"]+"/etc/alembic.ini"

    # Apply database schema to the provided endpoint
    print("Rucio configuration file: ", rucio_cfg_file)
    print("Alembic.ini configuration file: ", alembic_cfg_file)
    print("Applying the Rucio database schema to database endpoint: "+config_get('database', 'default')+"... ", end='', flush=True)
    engine = get_temp_engine(echo=echo)
    register_models(engine)
    print("done")

    # Put the database under version control
    print("Stamping databse version in alembic... ", end='', flush=True)
    alembic_cfg = Config(alembic_cfg_file)
    command.stamp(alembic_cfg, "head")
    print("done")

if __name__ == "__main__":
    init_rucio_database()