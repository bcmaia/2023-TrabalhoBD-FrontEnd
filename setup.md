
Se você não tiver o venv instalado: 
```
    python3 -m pip install --user virtualenv
```

Em sistemas baseados em debian, você pode precisar instalar o venv por meio do
 seguinte comando: 
```
    apt install python3.10-venv
```

Para criar o venv, vá para o diretório da aplicação e execute

```
    python -m venv venv
```

Para habilidar o ambiente virtual:
```
    source ./venv/bin/activate
```

Para instalar os módulos necessários: 
```
    pip install -r requirements.txt
```

Para executar o programa: 
```
    python3 main.py
```