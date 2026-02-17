# Instalação e Desenvolvimento

## Instalação para Usuários

### Via arquivo ZIP

1. Faça o download do arquivo `.zip` na [página de releases](https://github.com/tharlestsa/qgis-lgw/releases).
2. No QGIS, acesse `Plugins` → `Manage and Install Plugins...` → aba `Install from ZIP`.
3. Selecione o arquivo `.zip` obtido e clique em **Install Plugin**.
4. Após a instalação, o plugin estará disponível em `Plugins` → `Layer Grid View`.

## Ambiente de Desenvolvimento

### Pré-requisitos

- QGIS 3.0 ou superior instalado
- Python 3 (incluído com o QGIS)
- `pyrcc5` (incluído com o QGIS)
- `make`

### Deploy Local

Para instalar o plugin diretamente no diretório de plugins do QGIS:

```bash
make deploy
```

O comando copia os arquivos do plugin para:

```
~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/layer_grid_view/
```

Após o deploy, reinicie o QGIS ou utilize o plugin **Plugin Reloader** para recarregar sem reiniciar.

### Comandos Disponíveis

```bash
make help       # Exibe os comandos disponíveis
make deploy     # Instala o plugin no diretório local do QGIS
make test       # Executa os testes com pytest
make validate   # Valida a estrutura do plugin para o repositório OSGEO
make publish    # Gera o arquivo ZIP para publicação no plugins.qgis.org
make clean      # Remove arquivos gerados (__pycache__, .pyc, .pytest_cache)
make pylint     # Executa o linter
```

### Validação

O comando `make validate` verifica:

- Presença dos arquivos obrigatórios (`__init__.py`, `metadata.txt`, `icon.png`, `resources.py`)
- Existência das chaves obrigatórias no `metadata.txt` (`name`, `version`, `qgisMinimumVersion`, `description`, `author`, `email`, `tracker`, `repository`)
- Formato da versão (padrão semântico `X.Y.Z`)
- Validade das URLs de tracker e repository

### Publicação

O comando `make publish` gera um arquivo `.zip` pronto para envio ao [repositório oficial de plugins do QGIS](https://plugins.qgis.org/). O processo inclui:

1. Compilação dos recursos (`resources.py`)
2. Validação completa da estrutura
3. Empacotamento dos arquivos necessários (excluindo `__pycache__`, `.pyc`, `.git`)
4. Verificação de que o arquivo não excede 20 MB
