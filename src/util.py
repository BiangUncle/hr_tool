import pandas as pd

company_surfix = '（合丹）'

def DeleteNameSurfix(name: str) -> str:
    if name.endswith(company_surfix):
        return name[:len(name) - len(company_surfix)]
    
    return name


def default_set(df: pd.DataFrame, default_set_map: dict):
    for k, v in default_set_map.items():
        df[k].fillna(v, inplace=True)
    

def ContainFilePrefix(file_name: str, prefix_list: list) -> str:
    for prefix in prefix_list:
        if file_name.startswith(prefix):
            return prefix
        
    return ''

def GetTime10Before(time_str: str) -> str:
    return time_str[:10]