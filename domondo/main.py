import pandas as pd
from threads.ScrapBasicThread import ScrapBasicThread
from threads.ScrapPremiumThread import ScrapPremiumThread
from threads.ScrapNetThread import ScrapNetThread
from threads.ScrapArmorThread import ScrapArmorThread

roller_basic_thread = ScrapBasicThread()
roller_premium_thread = ScrapPremiumThread()
roller_net_thread = ScrapNetThread()
armor_thread = ScrapArmorThread()

roller_basic_thread.start()
roller_premium_thread.start()
roller_net_thread.start()
armor_thread.start()

roller_basic_thread.join()
roller_premium_thread.join()
roller_net_thread.join()
armor_thread.join()

roller_basic_pcv37 = roller_basic_thread.df_roller_pcv37
roller_basic_alu39 = roller_basic_thread.df_roller_alu39

roller_premium_pvc37 = roller_premium_thread.df_roller_pvc37
roller_premium_pvc52 = roller_premium_thread.df_roller_pvc52
roller_premium_alu39 = roller_premium_thread.df_roller_alu39
roller_premium_alu52 = roller_premium_thread.df_roller_alu52

roller_net_pvc37 = roller_net_thread.df_roller_pvc37
roller_net_alu39 = roller_net_thread.df_roller_alu39

armor_pvc37 = armor_thread.df_armor_pvc37
armor_pvc52 = armor_thread.df_armor_pvc52
armor_alu39 = armor_thread.df_armor_alu39
armor_alu52 = armor_thread.df_armor_alu52

dfs_roller_basic = {
    'Roleta PVC 37': roller_basic_pcv37,
    'Roleta ALU 39': roller_basic_alu39
}

dfs_roller_premium = {
    'Roleta PCV 37': roller_premium_pvc37,
    'Roleta PVC 52': roller_premium_pvc52,
    'Roleta ALU 39': roller_premium_alu39,
    'Roleta ALU 52': roller_premium_alu52
}

dfs_roller_net = {
    'Roleta z siatką PVC 37': roller_net_pvc37,
    'Roleta z siatką ALU 39': roller_net_alu39
}

dfs_armors = {
    'Pancerz PVC 37': armor_pvc37,
    'Pancerz PVC 57': armor_pvc52,
    'Pancerz ALU 39': armor_alu39,
    'Pancerz ALU 52': armor_alu52
}

with pd.ExcelWriter('Rolety_i_pancerze-Domondo_dict.xlsx') as writer:
    startrow = 1
    for name, roller in dfs_roller_basic.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety Basic')
        writer.sheets['Rolety Basic'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3)
    
    startrow = 1
    for name, roller in dfs_roller_premium.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety Premium')
        writer.sheets['Rolety Premium'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3) 
    
    startrow = 1
    for name, roller in dfs_roller_net.items():
        roller.to_excel(writer, startrow=startrow, sheet_name='Rolety z siatką')
        writer.sheets['Rolety z siatką'].cell(startrow,1).value=name
        startrow += (roller.shape[0] + 3) 
    
    startrow = 1
    for name, armor in dfs_armors.items():
        armor.to_excel(writer, startrow=startrow, sheet_name='Pancerze')
        writer.sheets['Pancerze'].cell(startrow,1).value=name
        startrow += (armor.shape[0] + 3) 
