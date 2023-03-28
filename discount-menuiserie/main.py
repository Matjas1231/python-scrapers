import pandas as pd
from threads.ScrapGateThread import ScrapGateThread

gate55_thread = ScrapGateThread(55)
gate77_thread = ScrapGateThread(77)

gate55_thread.start()
gate77_thread.start()

gate55_thread.join()
gate77_thread.join()

dfs_gate = {
    'Brama 55': gate55_thread.df_gate,
    'Brama 77': gate77_thread.df_gate
}

with pd.ExcelWriter('Bramy-discount-menuiserie.xlsx') as writer:
    startrow = 1
    for name, gate in dfs_gate.items():
        gate.to_excel(writer, startrow=startrow, sheet_name='Bramy')
        writer.sheets['Bramy'].cell(startrow,1).value=name
        startrow += (gate.shape[0] + 3)