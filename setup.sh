module load python
python -m venv env
source env/bin/activate

pip install -U pip
pip install numpy pandas scipy numba jiwer nltk
