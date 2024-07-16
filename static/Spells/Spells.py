from utils import Imports as I, Frequent_functions as Ff
class Spells:
    def __init__(self):
        self.spell_dict = {}
        self.generate_spells()
        self.selected_spell = {}
        self.direction = {}
        self.init_cast = {}
        self.spell_cooloff = {}

    def generate_spells(self):
        db_data = Ff.read_data_from_db("spells", ["name", "damage", "type", "direction", "mana", "knockback", "level", "recharge", "description"])
        a = 0
        b = 0
        for data in db_data:
            self.spell_dict[data[0]] = {
                "damage": data[1],
                "type": data[2],
                "direction": data[3],
                "mana": data[4],
                "knockback": data[5],
                "level": data[6],
                "recharge": data[7],
                "description": data[8],
            }
            I.info.SPELLBOOK_CONTENT[data[0]] = (a, b)
            if a >= 28:
                a = 0
                b += 2
            a += 2
