git init rucio-git
cd rucio-git
git remote add -f origin https://github.com/rucio/rucio.git

git config core.sparseCheckout true

echo "lib/rucio/common" >> .git/info/sparse-checkout
echo "lib/rucio/db" >> .git/info/sparse-checkout

git pull origin master

mkdir ../rucio

mv lib/rucio ../

cd ../rucio

touch __init__.py

cd ..

rm -rf rucio-git

python3 init_rucio_database.py
