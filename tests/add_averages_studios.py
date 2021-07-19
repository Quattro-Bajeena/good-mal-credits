from jikanpy import Jikan
import time, sys
from pathlib import Path
from time import sleep

sys.path.append(str(Path(__file__).resolve().parent.parent))

from anime_credits_app.models import Studio
from anime_credits_app import db
import anime_data_collector as adc


def update_studios_info():
    pass


def update_studios_averages():

    studios = Studio.query.all()
    for studio_db in studios:
        
        print(studio_db)

        #studio_mal = adc.mal.get_studio_api(studio_db.mal_id)
        studio_mal = adc.mal.get_resource('studios', studio_db.mal_id, True)
        members_sum = 0
        score_sum = 0

        score_count = 0
        member_count = 0

        for anime in studio_mal['anime']:
            if anime['score']:
                score_sum += anime['score']
                score_count += 1
            
            if anime['members']:
                members_sum += anime['members']
                member_count += 1


        studio_db.average_score = score_sum / score_count
        studio_db.average_members = members_sum / member_count
        studio_db.sum_members = members_sum

        adc.mal.save_studio(studio_mal)
        db.session.commit()

if __name__ == "__main__":
    update_studios_averages()