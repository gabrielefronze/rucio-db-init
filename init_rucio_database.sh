TAG=$1

GIT_REPO_URL="https://github.com/rucio/rucio"

mkdir rucio

if [[ ! -z "$TAG" && "$TAG" != "master" ]]; then
    svn export "$GIT_REPO_URL"/branches/"$TAG"/lib/rucio/common rucio/common
    svn export "$GIT_REPO_URL"/branches/"$TAG"/lib/rucio/db rucio/db
else
    svn export "$GIT_REPO_URL"/trunk/lib/rucio/common rucio/common
    svn export "$GIT_REPO_URL"/trunk/lib/rucio/db rucio/db
fi

touch ./rucio/__init__.py

if [[ ! -z "$RUCIO_HOME" ]]; then
    OLD_RUCIO_HOME="$RUCIO_HOME"
fi

export RUCIO_HOME=/opt/rucio-db-init

python3 init_rucio_database.py

unset RUCIO_HOME

if [[ ! -z "$OLD_RUCIO_HOME" ]]; then
    export RUCIO_HOME="$OLD_RUCIO_HOME"
fi

rm -rf rucio

unset GIT_REPO_URL
