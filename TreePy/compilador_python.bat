@echo off
:: Altera para o diretório onde o script está localizado
cd /d %~dp0

:menu
cls
echo =====================================
echo     PYTHON FILE SELECTION MENU
echo =====================================
echo Listando arquivos Python na pasta atual...
setlocal enabledelayedexpansion

:: Lista os arquivos .py e armazena em uma lista
set index=1
for %%f in (*.py) do (
    echo !index!. %%f
    set "file_!index!=%%f"
    set /a index+=1
)

set /a total_files=index-1

if %total_files%==0 (
    echo Nenhum arquivo Python encontrado na pasta atual.
    pause
    goto fim
)

echo =====================================
set /p escolha="Escolha o numero do arquivo para compilar: "

:: Verifica se a escolha é válida
if %escolha% LSS 1 (
    echo Opcao invalida.
    pause
    goto menu
)

if %escolha% GTR %total_files% (
    echo Opcao invalida.
    pause
    goto menu
)

:: Compila o arquivo selecionado
set "arquivo_selecionado=!file_%escolha%!"
echo =====================================
echo Escolha o tipo de compilacao:
echo 1. Compilar com interface grafica (com console)
echo 2. Compilar sem interface grafica (sem console)
echo =====================================
set /p tipo_compilacao="Escolha 1 ou 2: "

if %tipo_compilacao%==1 (
    echo Compilando o arquivo %arquivo_selecionado% com interface grafica...
    pyinstaller --onefile "%arquivo_selecionado%"
) else if %tipo_compilacao%==2 (
    echo Compilando o arquivo %arquivo_selecionado% sem interface grafica...
    pyinstaller --onefile --noconsole "%arquivo_selecionado%"
) else (
    echo Opcao invalida.
    pause
    goto menu
)

echo Compilacao concluida. O executavel esta na pasta dist.
pause
goto menu

:fim
echo Saindo...
pause
