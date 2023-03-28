import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread

roller_pvc44_motor_thread = ScrapRollerThread('https://www.volet-system.com/volet-roulant-renovation-aluminium-ou-pvc/181-volet-roulant-renovation-electrique-pvc.html')
roller_alu56_motor_thread = ScrapRollerThread('https://www.volet-system.com/volet-roulant-renovation-aluminium-ou-pvc/180-volet-roulant-renovation-electrique-grande-largeur.html')
roller_alu43_motor_thread = ScrapRollerThread('https://www.volet-system.com/volet-roulant-renovation-aluminium-ou-pvc/122-roulant-renovation-aluminium-electrique-radio.html')
roller_alu43_motor_promo_thread = ScrapRollerThread('https://www.volet-system.com/volet-roulant-renovation-aluminium-ou-pvc/277-roulant-renovation-aluminium-electrique-radio-promo.html')

roller_pvc44_motor_thread.start()
roller_alu43_motor_thread.start()
roller_alu43_motor_promo_thread.start()
roller_alu56_motor_thread.start()

roller_pvc44_motor_thread.join()
roller_alu43_motor_thread.join()
roller_alu43_motor_promo_thread.join()
roller_alu56_motor_thread.join()

dfs_roller_pvc = {
    'Roleta PVC 40 z silnikiem': roller_pvc44_motor_thread.df_roller
}

dfs_roller_alu = {
    'Roleta ALU 43 z silnikiem': roller_alu43_motor_thread.df_roller,
    'Roleta ALU 43 z silnikiem PROMOCYJNA': roller_alu43_motor_promo_thread.df_roller,
    'Roleta ALU 56 z silnikiem': roller_alu56_motor_thread.df_roller
}

with pd.ExcelWriter('Rolety-volet-system.xlsx') as writer:
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
