from utils import Imports as I
class Spells:
    def __init__(self):
        self.spell_dict = {}
        self.generate_spells()
        self.selected_spell = {}
        self.direction = {}
        self.init_cast = {}
        self.spell_cooloff = {}

    def generate_spells(self):
        I.info.SPELLBOOK_CONTENT.keys()
        for name, (desc, row, collumn) in I.info.SPELLBOOK_CONTENT.items():
            self.spell_dict[name] = desc
