alias commit='. ~/scripts/commit.sh'
alias push='. ~/scripts/push.sh'
alias biowiki='ssh root@198.211.110.229'
alias migrate="python3 manage.py makemigrations && python3 manage.py migrate"
alias reset="rm db.sqlite3 && migrate"
alias run="python3 manage.py runserver"
alias updatecardsna="python3 manage.py updatecardsna"
alias updatecardsjp="python3 manage.py updatecardsjp"
alias updateguerrilla="python3 manage.py updateguerrilla"
alias updateall="updatecardsna && updatecardsjp && updatedungeons && updateguerrilla"
alias updatedungeons="python3 manage.py updatedungeons"
alias maintenanceon="python3 manage.py maintenance_mode on"
alias maintenanceoff="python3 manage.py maintenance_mode off"

