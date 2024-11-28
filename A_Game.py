from Backend import Setup_pygame as SP
import os
from Values import Settings as S
S.local_path = os.getcwd()
print("YOUR PATH: ", S.local_path)

# import cProfile
#
# if __name__ == "__main__":
#     cProfile.run("SP.Set_up()", sort="time")


SP.Set_up()