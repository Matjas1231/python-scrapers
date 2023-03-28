import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread
from threads.ScrapArmorThread import ScrapArmorThread

roller_pvc_manual_thread = ScrapRollerThread('pvc')
roller_pvc_motor_thread = ScrapRollerThread('pvc', True)
roller_alu39_manual_thread = ScrapRollerThread('alu39')
roller_alu39_motor_thread = ScrapRollerThread('alu39', True)

roller_pvc_manual_thread.start()
roller_pvc_motor_thread.start()
roller_alu39_manual_thread.start()
roller_alu39_motor_thread.start()

roller_pvc_manual_thread.join()
roller_pvc_motor_thread.join()
roller_alu39_manual_thread.join()
roller_alu39_motor_thread.join()

roller_alu40_manual_thread = ScrapRollerThread('alu40')
roller_alu40_motor_thread = ScrapRollerThread('alu40', True)
roller_alu55_motor_thread = ScrapRollerThread('alu55', True)
armor_alu39_thread = ScrapArmorThread(39)

roller_alu40_manual_thread.start()
roller_alu40_motor_thread.start()
roller_alu55_motor_thread.start()
armor_alu39_thread.start()

roller_alu40_manual_thread.join()
roller_alu40_motor_thread.join()
roller_alu55_motor_thread.join()
armor_alu39_thread.join()

armor_alu40_thread = ScrapArmorThread(40)
armor_alu55_thread = ScrapArmorThread(55)
armor_alu77_thread = ScrapArmorThread(77)
roller_pvc_motor_net_thread = ScrapRollerThread('pvc', with_net=True)

armor_alu40_thread.start()
armor_alu55_thread.start()
armor_alu77_thread.start()
roller_pvc_motor_net_thread.start()

armor_alu40_thread.join()
armor_alu55_thread.join()
armor_alu77_thread.join()
roller_pvc_motor_net_thread.join()

roller_alu39_motor_net = ScrapRollerThread('alu39', with_net=True)

roller_alu39_motor_net.start()
roller_alu39_motor_net.join()

dfs_roller_pvc = {
    'Roleta PVC manual': roller_pvc_manual_thread.df_roller,
    'Roleta PVC silnik': roller_pvc_motor_thread.df_roller
}

dfs_roller_alu = {
    'Roleta ALU 39 manual': roller_alu39_manual_thread.df_roller,
    'Roleta ALU 39 silnik': roller_alu39_motor_thread.df_roller,
    'Roleta ALU 40 manual': roller_alu40_manual_thread.df_roller,
    'Roleta ALU 40 motor': roller_alu40_motor_thread.df_roller,
    'Roleta ALU 55 motor': roller_alu55_motor_thread.df_roller
}

dfs_armor_alu = {
    'Pancerz ALU 39': armor_alu39_thread.df_armor,
    'Pancerz ALU 40': armor_alu40_thread.df_armor,
    'Pancerz ALU 55': armor_alu55_thread.df_armor,
    'Pancerz ALU 77': armor_alu77_thread.df_armor
}

dfs_roller_net = {
    'Roleta PVC silnik siatka': roller_pvc_motor_net_thread.df_roller,
    'Roleta ALU 39 silnik siatka': roller_alu39_motor_net.df_roller
}

with pd.ExcelWriter('Rolety-leroidelafenetre.xlsx') as writer:
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
    for name, roller in dfs_roller_net.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety z siatką')
        writer.sheets['Rolety z siatką'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, armor in dfs_armor_alu.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze ALU')
        writer.sheets['Pancerze ALU'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)
