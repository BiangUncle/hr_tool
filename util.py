

company_surfix = '（合丹）'

def DeleteNameSurfix(name: str) -> str:
    if name.endswith(company_surfix):
        return name[:len(name) - len(company_surfix)]
    
    return name