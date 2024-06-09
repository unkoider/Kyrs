from app import db
from app.models import Player, Record

def update_player_record(player_id, level_name, time, score):
    record = Record.query.filter_by(player_id=player_id, level_name=level_name).first()
    
    if record:
        if time < record.record_t:
            record.record_t = time
        if score > record.record_s:
            record.record_s = score
    else:
        new_record = Record(player_id=player_id, level_name=level_name, record_t=time, record_s=score)
        db.session.add(new_record)
    
    db.session.commit()


