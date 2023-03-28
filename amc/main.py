import time
import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread
from threads.ScrapArmorThread import ScrapArmorThread

roller_pvc_thread = ScrapRollerThread('pvc')
roller_alu39_thread = ScrapRollerThread('alu39')
roller_alu52_thread = ScrapRollerThread('alu52')
armor_alu39_thread = ScrapArmorThread('alu39')
armor_alu52_thread = ScrapArmorThread('alu52')

roller_pvc_thread.start()
time.sleep(1)
roller_alu39_thread.start()
time.sleep(1)
roller_alu52_thread.start()
time.sleep(1)
armor_alu39_thread.start()
time.sleep(1)
armor_alu52_thread.start()
time.sleep(1)

roller_pvc_thread.join()
roller_alu39_thread.join()
roller_alu52_thread.join()
armor_alu39_thread.join()
armor_alu52_thread.join()

dfs_roller_pvc = {
    'Roleta PVC 39 Taśma': roller_pvc_thread.df_sangle,
    'Roleta PVC 39 Silnik': roller_pvc_thread.df_motor
}

dfs_roller_alu = {
    'Roleta ALU 39 Taśma': roller_alu39_thread.df_sangle,
    'Roleta ALU 39 Silnik': roller_alu39_thread.df_motor,
    'Roleta ALU 52 Taśma': roller_alu52_thread.df_sangle,
    'Roleta ALU 52 Silnik': roller_alu52_thread.df_motor
}

dfs_alu_net = {
    'Roleta ALU 39 z Siatką Taśma': roller_alu39_thread.df_net_sangle,
    'Roleta ALU 39 z Siatką Silnik': roller_alu39_thread.df_net_motor
}

dfs_armors = {
    'Pancerz ALU 39': armor_alu39_thread.df_armor,
    'Pancerz ALU 52': armor_alu52_thread.df_armor
}

with pd.ExcelWriter('Rolety_i_pancerze_amc.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller_pvc.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety PVC')
        writer.sheets['Roleta PVC'].cell(startrow, 1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_roller_alu.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety ALU')
        writer.sheets['Rolety ALU'].cell(startrow, 1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_alu_net.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety ALU z siatką')
        writer.sheets['Rolety ALU z siatką'].cell(startrow, 1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, armor in dfs_armors.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze ALU')
        writer.sheets['Pancerze ALU'].cell(startrow, 1).value=name
        startrow += (armor.shape[0] + 3)

