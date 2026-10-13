# Abre Chrome como un navegador NORMAL (sin automatizar) con el puerto de depuracion 9222 y un perfil propio
# fuera del repo. Inicia sesion en ChatGPT y pasa la verificacion de "soy humano" aqui, a mano.
# Despues: python herramientas/chatgpt_imagenes.py --conectar --hoja --foto F1 F2
$perfil = Join-Path $env:USERPROFILE ".unlock-chatgpt-debug"
$chrome = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chrome) { Write-Error "No encuentro chrome.exe"; exit 1 }
Start-Process $chrome -ArgumentList "--remote-debugging-port=9222", "--user-data-dir=`"$perfil`"", "--no-first-run", "https://chatgpt.com/"
