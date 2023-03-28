import time
import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread

roller_pvc_thread = ScrapRollerThread('pvc')
roller_alu39_thread = ScrapRollerThread('alu39')
roller_alu52_thread = ScrapRollerThread('alu52')

roller_pvc_thread.start()
time.sleep(1)
roller_alu39_thread.start()
time.sleep(1)
roller_alu52_thread.start()

roller_pvc_thread.join()
roller_alu39_thread.join()
roller_alu52_thread.join()

dfs_roller_pvc = {
    'Roleta PVC 39 Taśma': roller_pvc_thread.df_sangle,
    'Roleta PVC 39 Silnik': roller_pvc_thread.df_motor
}

dfs_roller_alu39 = {
    'Roleta ALU 39 Taśma': roller_alu39_thread.df_sangle,
    'Roleta ALU 39 Silnik': roller_alu39_thread.df_motor
}

dfs_roller_alu39_net = {
    'Roleta ALU 39 z Siatką Taśma': roller_alu39_thread.df_net_sangle,
    'Roleta ALU 39 z Siatką Silnik': roller_alu39_thread.df_net_motor
}

dfs_roller_alu52 = {
        'Roleta ALU 52 Taśma': roller_alu52_thread.df_sangle,
        'Roleta ALU 52 Silnik': roller_alu52_thread.df_motor
}

with pd.ExcelWriter('Rolety_store-volet.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller_pvc.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Roleta PVC')
        writer.sheets['Roleta PVC'].cell(startrow, 1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_roller_alu39.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Roleta ALU39')
        writer.sheets['Roleta ALU39'].cell(startrow, 1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_roller_alu39_net.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Roleta ALU39 z siatką')
        writer.sheets['Roleta ALU39 z siatką'].cell(startrow, 1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_roller_alu52.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Roleta ALU52')
        writer.sheets['Roleta ALU52'].cell(startrow, 1).value=name
        startrow += (roller.shape[0] + 3)
