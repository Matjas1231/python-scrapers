import time
import pandas as pd
from threads.ScraperThread import ScraperThread

roller39_thread = ScraperThread(39 ,'roller')
roller45_thread = ScraperThread(45, 'roller')
roller52_thread = ScraperThread(52, 'roller')
gate55_thread = ScraperThread(55, 'gate')
gate77_thread = ScraperThread(77, 'gate')

roller39_thread.start()
time.sleep(1)
roller45_thread.start()
time.sleep(1)
roller52_thread.start()
time.sleep(1)
gate55_thread.start()
time.sleep(1)
gate77_thread.start()

roller39_thread.join()
roller45_thread.join()
roller52_thread.join()
gate55_thread.join()
gate77_thread.join()

dfs_roller = {
    'Roleta 39 z silnikiem': roller39_thread.df,
    'Roleta 45 z silnikiem': roller45_thread.df,
    'Roleta 52 z silnikiem': roller52_thread.df
}

dfs_gate = {
    'Brama 55': gate55_thread.df,
    'Brama 77': gate77_thread.df
}

with pd.ExcelWriter('Rolety_i_bramy-nao-fermetures.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety')
        writer.sheets['Rolety'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)
        
    startrow = 1
    for name, gate in dfs_gate.items():
        gate.to_excel(writer, startrow=startrow, sheet_name='Bramy')
        writer.sheets['Bramy'].cell(startrow,1).value=name
        startrow += (gate.shape[0] + 3)
