import pandas as pd
from threads.ScrapRollerThread import ScrapRollerThread
from threads.ScrapGateThread import ScrapGateThread


roller_alu43_manual_thread = ScrapRollerThread(False)
roller_alu43_motor_thread = ScrapRollerThread(True)
gate_alu77_motor_thread = ScrapGateThread()

roller_alu43_manual_thread.start()
roller_alu43_motor_thread.start()
gate_alu77_motor_thread.start()

roller_alu43_manual_thread.join()
roller_alu43_motor_thread.join()
gate_alu77_motor_thread.join()

dfs_roller_alu = {
    'Roleta ALU 43 manual': roller_alu43_manual_thread.df_roller,
    'Roleta ALU 43 silnik': roller_alu43_motor_thread.df_roller,
}

dfs_gate_alu = {
    'Brama ALU 77 silnik': gate_alu77_motor_thread.df_gate
}

with pd.ExcelWriter('Rolety_i_bramy-1store1pro.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller_alu.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety ALU')
        writer.sheets['Rolety ALU'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)

    startrow = 1
    for name, gate in dfs_gate_alu.items():
        gate.to_excel(writer, startrow=startrow, sheet_name='Bramy ALU')
        writer.sheets['Bramy ALU'].cell(startrow,1).value=name
        startrow += (gate.shape[0] + 3)








