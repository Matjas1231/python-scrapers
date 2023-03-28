import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread
from threads.ScrapArmorThread import ScrapArmorThread

roller_alu40_motor_thread = ScrapRollerThread('alu40', with_motor=True)
roller_alu50_motor_thread = ScrapRollerThread('alu50', with_motor=True)
roller_alu55_motor_thread = ScrapRollerThread('alu55', with_motor=True)

roller_alu40_motor_thread.start()
roller_alu50_motor_thread.start()
roller_alu55_motor_thread.start()
roller_alu40_motor_thread.join()
roller_alu50_motor_thread.join()
roller_alu55_motor_thread.join()

roller_alu40_manual_thread = ScrapRollerThread('alu40', with_motor=False)
roller_alu50_manual_thread = ScrapRollerThread('alu50', with_motor=False)
roller_alu55_manual_thread = ScrapRollerThread('alu55', with_motor=False)

roller_alu40_manual_thread.start()
roller_alu50_manual_thread.start()
roller_alu55_manual_thread.start()

roller_alu40_manual_thread.join()
roller_alu50_manual_thread.join()
roller_alu55_manual_thread.join()

armor_alu40_thread = ScrapArmorThread('alu40')
armor_alu45_thread = ScrapArmorThread('alu45')
armor_alu55_thread = ScrapArmorThread('alu55')
armor_sp36_thread = ScrapArmorThread('sp36')

armor_alu40_thread.start()
armor_alu45_thread.start()
armor_alu55_thread.start()
armor_sp36_thread.start()

armor_alu40_thread.join()
armor_alu45_thread.join()
armor_alu55_thread.join()
armor_sp36_thread.join()

armor_pvc37_thread = ScrapArmorThread('pvc37')
armor_pvc42_thread = ScrapArmorThread('pvc42')

armor_pvc37_thread.start()
armor_pvc42_thread.start()

armor_pvc37_thread.join()
armor_pvc42_thread.join()

dfs_roller_alu = {
    'Roleta ALU 40 manual': roller_alu40_manual_thread.df_roller,
    'Roleta ALU 40 silnik': roller_alu40_motor_thread.df_roller,
    'Roleta ALU 50 manual': roller_alu50_manual_thread.df_roller,
    'Roleta ALU 50 silnik': roller_alu50_motor_thread.df_roller,
    'Roleta ALU 55 manual': roller_alu55_manual_thread.df_roller,
    'Roleta ALU 55 silnik': roller_alu55_motor_thread.df_roller
}

dfs_armor_alu = {
    'Pancerz ALU 40': armor_alu40_thread.df_armor,
    'Pancerz ALU 45': armor_alu45_thread.df_armor,
    'Pancerz ALU 55': armor_alu55_thread.df_armor,
    'Pancerz SP 36': armor_sp36_thread.df_armor
}

dfs_armor_pvc = {
    'Pancerz PVC 37': armor_pvc37_thread.df_armor,
    'Pancerz PVC 42': armor_pvc42_thread.df_armor,
}

with pd.ExcelWriter('Rolety_i_pancerze-boutique-pro-volet.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller_alu.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety ALU')
        writer.sheets['Rolety ALU'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)
    
    startrow = 1
    for name, armor in dfs_armor_alu.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze ALU')
        writer.sheets['Pancerze ALU'].cell(startrow,1).value=name
        startrow += (armor.shape[0] + 3)
    
    startrow = 1
    for name, armor in dfs_armor_pvc.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze PVC')
        writer.sheets['Pancerze PVC'].cell(startrow,1).value=name
        startrow += (armor.shape[0] + 3)
