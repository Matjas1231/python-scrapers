import time
import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread
from threads.ScrapArmorThread import ScrapArmorThread

roller39_manual_thread = ScrapRollerThread('rollladen39', False)
roller39_motor_thread = ScrapRollerThread('rollladen39', True)

roller39_manual_net_thread = ScrapRollerThread('rollladen39', False, True)
roller39_motor_net_thread = ScrapRollerThread('rollladen39', True, True)

roller52_manual_thread = ScrapRollerThread('rollladen52', False)
roller52_motor_thread = ScrapRollerThread('rollladen52', True)

roller77_motor_thread = ScrapRollerThread('rollladen77', True)

armor39_thread = ScrapArmorThread('39')
armor52_thread = ScrapArmorThread('52')
armor77_thread = ScrapArmorThread('77')


roller39_manual_thread.start()
time.sleep(1)
roller39_motor_thread.start()
time.sleep(1)
roller39_manual_net_thread.start()
time.sleep(1)
roller39_motor_net_thread.start()
time.sleep(1)
roller52_manual_thread.start()
time.sleep(1)
roller52_motor_thread.start()
time.sleep(1)
roller77_motor_thread.start()
time.sleep(1)
armor39_thread.start()
time.sleep(1)
armor52_thread.start()
time.sleep(1)
armor77_thread.start()
time.sleep(1)

roller39_manual_thread.join()
roller39_motor_thread.join()
roller39_manual_net_thread.join()
roller39_motor_net_thread.join()
roller52_manual_thread.join()
roller52_motor_thread.join()
roller77_motor_thread.join()
armor39_thread.join()
armor52_thread.join()
armor77_thread.join()

dfs_roller39 = {
        'Roleta 39 z Taśmą': roller39_manual_thread.df_roller,
        'Roleta 39 z Silnikiem': roller39_motor_thread.df_roller
}

dfs_roller39_net = {
    'Roleta 39 z siatką z Taśmą': roller39_manual_net_thread.df_roller,
    'Roleta 39 z zsiatką Silnikiem': roller39_motor_net_thread.df_roller
}

dfs_roller52 = {
    'Roleta 52 z taśmą': roller52_manual_thread.df_roller,
    'Roleta 52 z Silnik': roller52_motor_thread.df_roller
}

dfs_roller77 = {
    'Roleta 77 z silnikiem': roller77_motor_thread.df_roller
}

dfs_armors = {
    'Pancerz 39': armor39_thread.df_armor,
    'Pancerz 52': armor52_thread.df_armor,
    'Pancerz 77': armor77_thread.df_armor
}

with pd.ExcelWriter('Rolety_i_pancerze-rollerieper-52-silnik.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller39.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety 39')
        writer.sheets['Rolety 39'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_roller39_net.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety 39 z siatką')
        writer.sheets['Rolety 39 z siatką'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)
        
    startrow = 1
    for name, roller in dfs_roller52.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety 52')
        writer.sheets['Rolety 52'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)
        
    startrow = 1
    for name, armor in dfs_roller77.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Rolety 77')
        writer.sheets['Rolety 77'].cell(startrow, 1).value=name
        startrow += (armor.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_armors.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Pancerze')
        writer.sheets['Pancerze'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)


