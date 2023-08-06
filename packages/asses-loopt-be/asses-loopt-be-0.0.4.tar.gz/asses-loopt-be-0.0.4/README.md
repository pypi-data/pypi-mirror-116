# asses-loopt-be

### Install
```sh
pip install asses-loopt-be
```

### Usage
```python
from AssesLooptBE import AssesLooptBE as asses

df = pd.read_csv('./dfteste.csv') # input DataFrame
asses_be = asses.AssesLooptBE(df) # instantiating class

asses_be.help() # call functions
```

### Functions
- acertos_medios_porcentagem()
- acertos_medios_pol()
- acertos_medios_porcentagem_embarques()
- acerto_variacao_porcentagem_fe_bookado()
- acerto_variacao_porcentagem_predict_bookado()
- acertos_medios_porcentagem_day()
- acertos_medios_porcentagem_embarque_day()
- matriz_confusao()
- distribuicoes()


All functions you must pass a boolean parameter if you want it to return the value, otherwise it will just update its instantiated object

# Last Version
0.0.3