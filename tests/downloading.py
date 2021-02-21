import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from anime_credits_app.mal_db import update_characters_staff, update_person_credits


#update_characters_staff(2136, True)
update_person_credits(21, True)