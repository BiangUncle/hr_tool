

def NameResolver(name: str) -> str:
    if name.endswith('（合丹）'):
        name = name.replace('（合丹）', '')
    
    return name