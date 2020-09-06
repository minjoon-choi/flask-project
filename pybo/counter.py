from flask import session
from sqlalchemy import func
import time
from .models import Idea

class generate_num():
    def generate_ideaNum():
        count2 = session.query(func.count(Idea.id)).scalar()
        YYYYMM = time.strftime('%Y-%m', time.localtime(time.time()))
        return print(str(count)+'-'+str(YYYYMM))
