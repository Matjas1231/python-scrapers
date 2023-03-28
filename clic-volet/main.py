import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread
from threads.ScrapArmorThread import ScrapArmorThread
from threads.ScrapGateThread import ScrapGatehread

armor_thread = ScrapArmorThread()
roller_manual_threads = ScrapRollerThread(False)
roller_motor_threads = ScrapRollerThread(True)
gatepx75_thread = ScrapGatehread()

roller_manual_threads.start()
roller_motor_threads.start()
armor_thread.start()
gatepx75_thread.start()

roller_manual_threads.join()
roller_motor_threads.join()
armor_thread.join()
gatepx75_thread.join()

dfs_roller_pvc = {
    'Roleta PVC 40 z taśmą': roller_manual_threads.df_roller_pvc40,
    'Roleta PVC 40 z silnikiem': roller_motor_threads.df_roller_pvc40
}

dfs_roller_alu = {
    'Roleta ALU 39 z taśmą': roller_manual_threads.df_roller_alu39,
    'Roleta ALU 39 z silnikiem': roller_motor_threads.df_roller_alu39,
    'Roleta ALU 40 z taśmą': roller_manual_threads.df_roller_alu40,
    'Roleta ALU 40 z silnikiem': roller_motor_threads.df_roller_alu40,
    'Roleta ALU 39 Thermoflex z taśmą': roller_manual_threads.df_roller_alu_thermoreflex_39,
    'Roleta ALU 39 Thermoflex z silnikiem': roller_motor_threads.df_roller_alu_thermoreflex_39
}

dfs_armor_pvc = {
    'Pancerz PVC 40': armor_thread.df_armor_pvc40,
    'Pancerz PVC 60': armor_thread.df_armor_pvc60
}

dfs_armor_alu = {
    'Pancerz ALU 39': armor_thread.df_armor_alu39,
    'Pancerz ALU 40': armor_thread.df_armor_alu40,
    'Pancerz ALU 55': armor_thread.df_armor_alu55,
    'Pancerz ALU 39 Thermoflex': armor_thread.df_armor_alu_thermoreflex_39
}

dfs_gate = {
    'Brama PX-75': gatepx75_thread.df_gate
}

with pd.ExcelWriter('Rolety_pancerze_bramy-clic-volet.xlsx') as writer:
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
    for name, armor in dfs_armor_pvc.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze PVC')
        writer.sheets['Pancerze PVC'].cell(startrow,1).value=name
        startrow += (armor.shape[0] + 3)

    startrow = 1
    for name, armor in dfs_armor_alu.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze ALU')
        writer.sheets['Pancerze ALU'].cell(startrow,1).value=name
        startrow += (armor.shape[0] + 3)

    startrow = 1
    for name, gate in dfs_gate.items():
        gate.to_excel(writer, startrow=startrow, sheet_name='Bramy')
        writer.sheets['Bramy'].cell(startrow,1).value=name
        startrow += (gate.shape[0] + 3)