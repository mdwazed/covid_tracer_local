
# from app_user.models import PersInfo

rank_choices = [
    ('', '--------'),
    ('Snk', 'Snk'),
    ('Lcpl', 'Lcpl'),
    ('Cpl', 'Cpl'),
    ('Sgt', 'Sgt'),
    ('WO', 'WO'),
    ('SWO', 'SWO'),
    ('MWO', 'MWO'),
    ('2 Lt', '2 Lt'),
    ('Lt', 'Lt'),
    ('Capt', 'Capt'),
    ('Maj', 'Maj'),
    ('Lt_Col', 'Lt Col'),
    ('Col', 'Col'),
    ('Brig Gen', 'Brig Gen'),
    ('Maj Gen', 'Maj Gen'),
]

class ContactedUser():
    """ hybrid obj of back end and local user """
    def __init__(self, user, contact_time):
        self.user_gen_id = user.user_gen_id
        self.app_gen_id = user.app_gen_id
        
        self.name = user.name
        self.contact_time = contact_time

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.app_gen_id == other.app_gen_id

    def __hash__(self):
        return int(self.app_gen_id)

