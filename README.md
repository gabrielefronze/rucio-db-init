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