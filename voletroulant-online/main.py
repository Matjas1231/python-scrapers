import time
import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread
from threads.ScrapArmorThread import ScrapArmorThread

roller_pvc_manual_thread = ScrapRollerThread('pvc', False)
roller_pvc_motor_thread = ScrapRollerThread('pvc', True)

roller_alu_manual_thread = ScrapRollerThread('alu', False)
roller_alu_motor_thread = ScrapRollerThread('alu', True)

armor_pvc_thread = ScrapArmorThread('pvc')
armor_alu_thread = ScrapArmorThread('alu')

roller_pvc_manual_thread.start()
time.sleep(1)
roller_pvc_motor_thread.start()
time.sleep(1)
roller_alu_manual_thread.start()
time.sleep(1)
roller_alu_motor_thread.start()
time.sleep(1)
armor_pvc_thread.start()
time.sleep(1)
armor_alu_thread.start()
time.sleep(1)

roller_pvc_manual_thread.join()
roller_pvc_motor_thread.join()
roller_alu_manual_thread.join()
roller_alu_motor_thread.join()
armor_pvc_thread.join()
armor_alu_thread.join()

dfs_roller_pvc = {
    'Roleta PVC z taśmą': roller_pvc_manual_thread.df_roller,
    'Roleta PVC z silnikiem': roller_pvc_motor_thread.df_roller
}

dfs_roller_alu = {
    'Roleta ALU z taśmą': roller_alu_manual_thread.df_roller,
    'Roleta ALU z silnikiem': roller_alu_motor_thread.df_roller
}

dfs_armor = {
    'Pancerz PVC': armor_pvc_thread.df_armor,
    'Pancerz ALU': armor_alu_thread.df_armor
}

with pd.ExcelWriter('Rolety_i_pancerze-voletroulant.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller_pvc.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety PVC')
        writer.sheets['Rolety PVC'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_roller_alu.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety ALU')
        writer.sheets['Rolety ALU'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, armor in dfs_armor.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze')
        writer.sheets['Pancerze'].cell(startrow,1).value=name
        startrow += (armor.shape[0] + 3)