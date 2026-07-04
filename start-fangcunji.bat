@echo off
title Fangcunji Stamp Website
cd /d "%~dp0"

rem If already running, just open the browser
netstat -ano | findstr ":3000" | findstr "LISTENING" >nul
if %errorlevel%==0 (
  start "" "http://localhost:3000"
  exit
)

echo ============================================
echo   方寸集邮票网站启动中，请稍候...
echo   启动后会自动打开浏览器
echo   注意：请保持本窗口开着，关闭窗口=停止网站
echo ============================================
start "" cmd /c "timeout /t 6 /nobreak >nul & start http://localhost:3000"
npm run dev
