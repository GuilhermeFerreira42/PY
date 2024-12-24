@echo off
setlocal enabledelayedexpansion

REM Define o arquivo de saída
set "output_file=resultado.txt"

REM Apaga o arquivo de saída se já existir
if exist "%output_file%" del "%output_file%"

REM Função para percorrer recursivamente as pastas e arquivos
call :process_folder "%cd%"

REM Adiciona a estrutura da árvore de pastas ao final do arquivo
echo. >> "%output_file%"
echo ========================================== >> "%output_file%"
echo Estrutura de pastas: >> "%output_file%"
echo ========================================== >> "%output_file%"
echo ``` >> "%output_file%"

REM Gera a árvore e salva no arquivo
tree /a /f >> "%output_file%"

echo ``` >> "%output_file%"

echo Operação concluída! Arquivos combinados e estrutura de pastas adicionada em "%output_file%".
pause
exit /b

:process_folder
set "current_folder=%~1"

REM Percorre os arquivos na pasta atual
for %%f in ("%current_folder%\*.*") do (
    if not "%%~ff"=="%output_file%" (
        echo ========================================== >> "%output_file%"
        echo Arquivo: %%~f >> "%output_file%"
        echo ========================================== >> "%output_file%"
        type "%%f" >> "%output_file%"
        echo. >> "%output_file%" REM Adiciona uma linha em branco para separação
    )
)

REM Percorre as subpastas recursivamente
for /d %%d in ("%current_folder%\*") do (
    call :process_folder "%%d"
)
exit /b
