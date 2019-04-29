# $1 is taken as tag, set to master if not specified
VERSION=${1:-master}

GIT_REPO_URL="https://github.com/rucio/rucio"

mkdir rucio

echo -n "Retrieving rucio $TAG... "
if [[ "$VERSION" != "master" && "$VERSION" != "hotfix" && "$VERSION" != "next" ]]; then
    svn export -q "$GIT_REPO_URL"/tags/"$VERSION"/lib/rucio/common rucio/common
    svn export -q "$GIT_REPO_URL"/tags/"$VERSION"/lib/rucio/db/sqla rucio/db/sqla
elif [[ "$VERSION" == "hotfix" || "$VERSION" == "next" ]]; then
    svn export -q "$GIT_REPO_URL"/branches/"$VERSION"/lib/rucio/common rucio/common
    svn export -q "$GIT_REPO_URL"/branches/"$VERSION"/lib/rucio/db/sqla rucio/db/sqla
else
    svn export -q "$GIT_REPO_URL"/trunk/lib/rucio/common rucio/common
    svn export -q "$GIT_REPO_URL"/trunk/lib/rucio/db/sqla rucio/db/sqla
fi
echo "done"

echo -n "Initializing python workspace... "
touch ./rucio/__init__.py
touch ./rucio/db/__init__.py
echo "done"

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
