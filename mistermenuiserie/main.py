import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread


roller_alu39_manual_thread = ScrapRollerThread('https://www.mistermenuiserie.com/volet-roulant-renovation-manuel-aluminium-sur-mesure-solario-481366.html')
roller_alu39_motor_thread = ScrapRollerThread('https://www.mistermenuiserie.com/volet-roulant-renovation-filaire-aluminium-sur-mesure-solario-481342.html')

roller_alu39_manual_thread.start()
roller_alu39_motor_thread.start()
roller_alu39_manual_thread.join()
roller_alu39_motor_thread.join()


roller_alu40_motor_thread = ScrapRollerThread('https://www.mistermenuiserie.com/volet-roulant-aluminium-motorisation-filaire-pose-inversee.html')
roller_alu40_manual_thread = ScrapRollerThread('https://www.mistermenuiserie.com/volet-roulant-aluminium-manuel-pose-inversee.html')

roller_alu40_motor_thread.start()
roller_alu40_manual_thread.start()
roller_alu40_motor_thread.join()
roller_alu40_manual_thread.join()

roller_alu50_motor_thread = ScrapRollerThread('https://www.mistermenuiserie.com/volet-roulant-aluminium-motorisation-filaire-pose-inversee.html', True)
roller_alu50_manual_thread = ScrapRollerThread('https://www.mistermenuiserie.com/volet-roulant-aluminium-manuel-pose-inversee.html', True)

roller_alu50_motor_thread.start()
roller_alu50_manual_thread.start()
roller_alu50_motor_thread.join()
roller_alu50_manual_thread.join()

dfs_armor_alu39 = {
    'Pancerz ALU 39 z taśmą': roller_alu39_manual_thread.df_roller,
    'Pancerz ALU 39 z silnikiem': roller_alu39_motor_thread.df_roller
}

dfs_armor_alu40 = {
    'Pancerz ALU 40 z taśmą': roller_alu40_manual_thread.df_roller,
    'Pancerz ALU 40 z silnikiem': roller_alu40_motor_thread.df_roller
}

dfs_armor_alu50 = {
    'Pancerz ALU 50 z taśmą': roller_alu50_manual_thread.df_roller,
    'Pancerz ALU 50 z silnikiem': roller_alu50_motor_thread.df_roller
}

with pd.ExcelWriter('Rolety_i_pancerze-voletshop.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_armor_alu39.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety ALU 39')
        writer.sheets['Rolety ALU 39'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_armor_alu40.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety ALU 40')
        writer.sheets['Rolety ALU 40'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, roller in dfs_armor_alu50.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety ALU 50')
        writer.sheets['Rolety ALU 50'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)