from utils import Imports as I
from Backend import Setup_pygame as SP
from Values import Settings as S
def update_game():
    # Path to your local game repository
    repo_dir = S.local_path  # Change this to your repo directory
    print(repo_dir)
    # URL of the GitHub repository
    repo_url = "https://github.com/Kuramalt16/A_Game"

    # Check if the repository exists locally
    if not I.os.path.exists(repo_dir):
        # If not, clone it
        print("Cloning the repository...")
        I.git.Repo.clone_from(repo_url, repo_dir)
        print("Repository cloned.")
    else:
        # If it exists, pull the latest changes
        try:
            repo = I.git.Repo(repo_dir)
            print("Pulling the latest changes...")
            origin = repo.remotes.origin
            origin.pull()  # Pull the latest changes
            print("Repository updated.")
        except I.git.exc.GitCommandError as e:
            print(f"Error updating repository: {e}")
            return

    # After updating, restart the game
    print("Restart the game please!!!")
    I.pg.quit()  # Quit the current Pygame window
    I.sys.exit()  # Exit the current script
    # restart_game()

def restart_game():

    # Full path to the executable
    # exe_path = I.os.path.join(S.local_path, "dist\A_game.exe")
    #
    # try:
    #     # Run the .exe file using subprocess
    #     cmd_command = f'cmd.exe /k "{exe_path}"'
    #     I.subprocess.Popen(cmd_command, shell=True)  # Start cmd and run the executable
    #     print(f"Game started from {exe_path}")
    # except Exception as e:
    #     print(f"Error while trying to run the executable: {e}")
    #
    # # Quit the current instance of Pygame and exit
    # I.t.sleep(5)
    # I.pg.quit()  # Quit the current Pygame window
    # I.sys.exit()  # Exit the current script

    I.pg.quit()  # Quit the current Pygame window
    # I.sys.exit()  # Exit the current script
    S.START_APP = True
    S.MAIN_MENU = True
    S.BUSY = False
    SP.Set_up()