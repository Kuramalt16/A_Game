import pygame as pg
from PIL import Image as img
import os
import subprocess
import git
import sys
from Values import Available as A
from Values import Songs
from Data.Temp_data import values as TD
from datetime import datetime
from Testing import test as T, testing_displays as Test_dis
import time as t
from static.data.play_data import info
from static.data.play_data import mob_data
from static.data.play_data import gifs
from static.data.play_data import decor
from scipy.ndimage import zoom
from static.dialog import Dialog as dialog, Title_handle as Titles
from static.items import items
from static.Spells import Spells
from static.rooms import rooms
import shutil
import threading
import math
import heapq
import numpy as np
from static.data.Character_byte_data import CharacterData
import sqlite3
import random
import webcolors
import queue
from utils import threads as th
from Backend import (Tool_backend as TB, Spell_Backend as SB, Dialog_backend as DialB, Item_backend as IB,
                     guard_backend as GB, quests_backend as QB, appliance_backend as AB, Backpack_backend as BB,
                     Player_Backend as PB, shop_backend as SHB, Containers_backend as CB, folower_backend as FB,
                     Mob_Backend as MB, update_game as UG, map_backend as MapB, Plants_backend as PlantB, Sprites as S)