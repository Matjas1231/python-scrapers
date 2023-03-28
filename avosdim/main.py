from threads.ScrapPvcThread import ScrapPvcThread
from threads.ScrapAluThread import ScrapAluThread
import pandas as pd

roller_pvc_thread = ScrapPvcThread(False)
armor_pvc_thread = ScrapPvcThread(True)
roller_pvc_thread.start()
armor_pvc_thread.start()


roller_alu_thread = ScrapAluThread(False)
armor_alu_thread = ScrapAluThread(True)

roller_alu_thread.start()
armor_alu_thread.start()

roller_pvc_thread.join()
armor_pvc_thread.join()

roller_alu_thread.join()
armor_alu_thread.join()

dfs_roller = {
    'Roleta PVC': roller_pvc_thread.df,
    'Roleta ALU': roller_alu_thread.df
}

dfs_armors = {
    'Pancerz PCV': armor_pvc_thread.df,
    'Pancerz ALU': armor_alu_thread.df
}

with pd.ExcelWriter('Rolety_i_Pancerze-avosdim.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller:
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety')
        writer.sheets['Rolety'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)
        
    startrow = 1
    for name, armor in dfs_armors:
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze')
        writer.sheets['Pancerze'].cell(startrow, 1).value=name
        startrow += (armor.shape[0] + 3)
