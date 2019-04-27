git init rucio
cd rucio
git remote add -f origin https://github.com/rucio/rucio.git

git config core.sparseCheckout true

echo "lib/rucio/common" >> .git/info/sparse-checkout
echo "lib/rucio/db" >> .git/info/sparse-checkout

git pull origin master

cd ..

python3 init_rucio_database.py
