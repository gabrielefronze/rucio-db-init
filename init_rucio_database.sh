TAG=$1

git init rucio-git
cd rucio-git
git remote add -f origin https://github.com/rucio/rucio.git

git config core.sparseCheckout true

echo "lib/rucio/common" >> .git/info/sparse-checkout
echo "lib/rucio/db" >> .git/info/sparse-checkout

git pull origin master

if [[ ! -z "$TAG" ]]; then
    git checkout tags/"$TAG"
fi

mkdir ../rucio

mv lib/rucio ../

cd ../rucio

touch __init__.py

cd ..

rm -rf rucio-git

if [[ ! -z "$RUCIO_HOME" ]]; then
    OLD_RUCIO_HOME="$RUCIO_HOME"
fi

export RUCIO_HOME=/opt/rucio-db-init

python3 init_rucio_database.py

unset RUCIO_HOME

if [[ ! -z "$OLD_RUCIO_HOME" ]]; then
    export RUCIO_HOME="$OLD_RUCIO_HOME"
fi
