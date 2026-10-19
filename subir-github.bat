@echo off
chcp 65001 >nul
echo ============================================
echo  Enviando projeto para o GitHub...
echo  Usuario: pafarnezi
echo  Repositorio: api-gestao-despesas
echo ============================================

cd /d "%~dp0"

git init
if errorlevel 1 (
    echo ERRO: O Git nao esta instalado ou nao foi encontrado no PATH.
    echo Baixe em: https://git-scm.com/download/win
    pause
    exit /b 1
)

git branch -M main
git add .
git commit -m "feat: API de gestão de despesas com especificacao, ADR de testes e codigo funcional"
git remote add origin https://github.com/pafarnezi/api-gestao-despesas.git
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERRO ao enviar. Possiveis causas:
    echo - Voce precisa autenticar com Personal Access Token (PAT).
    echo - O repositorio ja existe no GitHub com conteudo diferente.
    echo.
    echo Para criar um PAT: github.com/settings/tokens -> escopo 'repo'
    pause
    exit /b 1
)

echo.
echo ============================================
echo  CONCLUIDO!
echo  Acesse: https://github.com/pafarnezi/api-gestao-despesas
echo ============================================
pause