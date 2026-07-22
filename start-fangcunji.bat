@echo off
chcp 65001 >nul
title 纸上山河 - 总门厅
cd /d "%~dp0"

rem 双击运行时 cmd.exe 的系统 PATH 里可能没有 node/npm，这里显式补上
set "PATH=G:\Program Files\nodejs;%PATH%"

where npm >nul 2>nul
if errorlevel 1 (
  echo ============================================
  echo   错误：找不到 npm，请确认 Node.js 是否已安装
  echo   期望路径：G:\Program Files\nodejs
  echo ============================================
  pause
  exit /b 1
)

rem 已经在跑就直接开浏览器
netstat -ano | findstr ":3000" | findstr "LISTENING" >nul
if %errorlevel%==0 (
  start "" "http://localhost:3000/stamps"
  exit /b 0
)

echo ============================================
echo   纸上山河 总站启动中，请稍候...
echo   浏览器将自动打开总门厅（邮票馆/画册馆/名画馆）
echo   注意：请保持本窗口开着，关闭窗口 = 停止网站
echo   如果这个窗口很快自己关闭，说明启动出错，
echo   请重新双击一次，仔细看这里打印的报错信息
echo ============================================
start "" cmd /c "timeout /t 6 /nobreak >nul & start http://localhost:3000/stamps"

call npm run dev
if errorlevel 1 (
  echo.
  echo ============================================
  echo   启动失败，上面是详细报错信息
  echo ============================================
  pause
)
