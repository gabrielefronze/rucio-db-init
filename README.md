# rucio-db-init
A standalone initializer for SQL databases used by Rucio

This is intended to run using python3.
It requires requests, alembic, sqlalchemy, jsonschema, psycopg2-binary and retrying.
Run the following command to install the needed dependencies:

```
pip3 install requests alembic sqlalchemy jsonschema psycopg2-binary retrying
```

Please note that this script requires one to set up the `$RUCIO_HOME` environment variable, which is automatically set by the `init-rucio-repo.sh` script.
`$RUCIO_HOME` must contain an `/etc` subfolder with `rucio.cfg` and `alembic.ini` configuration files inside.
The script is preconfigured to use the `/etc` directory embedded in this repo.

Due to the Rucio configuration structure it is not possible to simply pass two custom files directly.

The `init-rucio-repo.sh` introduces support for different rucio tags. The default tag is `master` but different tags can be used via:

```
    source init_rucio_database.sh 1.19.1
```

Please note that due to Rucio development, tags before 1.19.X are not supported due to the fact that in Python 3 `ConfigParser` has been renamed to `configparser`.