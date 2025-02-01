@echo off
cls

echo =========================================
echo Current Network Information:
echo =========================================
powershell -Command "(Get-NetIPConfiguration -InterfaceAlias 'Ethernet')"

echo =========================================
echo SELECT DNS SERVER
echo =========================================
echo 1. Google DNS (8.8.8.8 / 8.8.4.4) [IPv4] - (2001:4860:4860::8888 / 2001:4860:4860::8844) [IPv6]
echo 2. Cloudflare DNS (1.1.1.1 / 1.0.0.1) [IPv4] - (2606:4700:4700::1111 / 2606:4700:4700::1001) [IPv6]
echo 3. OpenDNS (208.67.222.222 / 208.67.220.220) [IPv4] - (2620:119:35::35 / 2620:119:53::53) [IPv6]
echo 4. Custom DNS
echo 5. Close
echo =========================================
set /p option="Select option (1-5): "

if "%option%"=="1" goto GoogleDNS
if "%option%"=="2" goto CloudflareDNS
if "%option%"=="3" goto OpenDNS
if "%option%"=="4" goto CustomDNS
if "%option%"=="5" exit

:GoogleDNS
echo Configuring Google DNS (8.8.8.8 / 8.8.4.4) [IPv4] and (2001:4860:4860::8888 / 2001:4860:4860::8844) [IPv6]...
netsh interface ipv4 set dns name="Ethernet" static 8.8.8.8
netsh interface ipv4 add dns name="Ethernet" 8.8.4.4 index=2
netsh interface ipv6 set dns name="Ethernet" static 2001:4860:4860::8888
netsh interface ipv6 add dns name="Ethernet" 2001:4860:4860::8844 index=2
goto End

:CloudflareDNS
echo Configuring Cloudflare DNS (1.1.1.1 / 1.0.0.1) [IPv4] and (2606:4700:4700::1111 / 2606:4700:4700::1001) [IPv6]...
netsh interface ipv4 set dns name="Ethernet" static 1.1.1.1
netsh interface ipv4 add dns name="Ethernet" 1.0.0.1 index=2
netsh interface ipv6 set dns name="Ethernet" static 2606:4700:4700::1111
netsh interface ipv6 add dns name="Ethernet" 2606:4700:4700::1001 index=2
goto End

:OpenDNS
echo Configuring OpenDNS (208.67.222.222 / 208.67.220.220) [IPv4] and (2620:119:35::35 / 2620:119:53::53) [IPv6]...
netsh interface ipv4 set dns name="Ethernet" static 208.67.222.222
netsh interface ipv4 add dns name="Ethernet" 208.67.220.220 index=2
netsh interface ipv6 set dns name="Ethernet" static 2620:119:35::35
netsh interface ipv6 add dns name="Ethernet" 2620:119:53::53 index=2
goto End

:CustomDNS
set /p dns1="First DNS (IPv4): "
set /p dns2="Second DNS (IPv4): "
set /p dns3="First DNS (IPv6): "
set /p dns4="Second DNS (IPv6): "
echo Configuring DNS %dns1% and %dns2% [IPv4] and %dns3% and %dns4% [IPv6]...
netsh interface ipv4 set dns name="Ethernet" static %dns1%
netsh interface ipv4 add dns name="Ethernet" %dns2% index=2
netsh interface ipv6 set dns name="Ethernet" static %dns3%
netsh interface ipv6 add dns name="Ethernet" %dns4% index=2
goto End

:End
echo Configuration completed!
echo =========================================
echo Current Network Information:
echo =========================================
powershell -Command "(Get-NetIPConfiguration -InterfaceAlias 'Ethernet')"

echo =========================================
pause
