from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

def set_follower_mob_target(mob, mob_class):
    I.info.FOLLOWER["aggressive"]["mob"] = mob
    I.info.FOLLOWER["aggressive"]["class"] = mob_class
    I.info.FOLLOWER["aggressive"]["mob_pos"] = mob["current_pos"]
    I.info.FOLLOWER["aggressive"]["attack"] = True