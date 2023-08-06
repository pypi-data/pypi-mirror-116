try:
    import xmltodict
except:
    raise ImportError('Unable to import xmltodict, please `pip install xmltodict==0.12.0`.')
else:
    if xmltodict.__version__ != '0.12.0':
        raise ImportError("xmltodict's version must be `0.12.0`, please `pip install xmltodict==0.12.0`.")

try:
    import yaml
except:
    raise ImportError('Unable to import yaml, please `pip install PyYAML==5.4.1`.')
else:
    if yaml.__version__ != '5.4.1':
        raise ImportError("PyYAML's version must be `5.4.1`, please `pip install PyYAML==5.4.1`.")
