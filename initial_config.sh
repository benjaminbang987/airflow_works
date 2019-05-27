# Initial setup of Airflow_works pyenv and package requirements

# Install pyenv
curl https://pyenv.run | bash
brew install pyenv
brew install zlib
brew install postgresql
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
pyenv install -s 3.6.2
pyenv virtualenv 3.6.2 airflow_works
pyenv activate airflow_works
pyenv local airflow_works # this takes care of the local fixation
pip install -r requirements.txt

