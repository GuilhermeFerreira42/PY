@echo off
setlocal enabledelayedexpansion

REM Define a pasta atual e o arquivo de saída
set "output_file=resultado.txt"
set "source_folder=%cd%"

REM Apaga o arquivo de saída se já existir
if exist "%output_file%" del "%output_file%"

REM Percorre todos os arquivos na pasta atual
for %%f in (*.*) do (
    REM Adiciona um cabeçalho com o nome do arquivo
    echo ========================================== >> "%output_file%"
    echo Arquivo: %%f >> "%output_file%"
    echo ========================================== >> "%output_file%"
    
    REM Adiciona o conteúdo do arquivo ao resultado
    type "%%f" >> "%output_file%"
    echo. >> "%output_file%" REM Adiciona uma linha em branco para separação
)

echo Arquivos combinados e salvos em "%output_file%".
pause
