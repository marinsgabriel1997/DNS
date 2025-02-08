@echo off
cls

echo =========================================
echo Current Network Information:
echo =========================================
powershell -Command "(Get-NetIPConfiguration -InterfaceAlias 'Ethernet')"

echo =========================================
echo SELECT DNS SERVER
echo =========================================
echo 1. Custom DNS
echo 2. Google DNS (8.8.8.8 / 8.8.4.4) [IPv4] - (2001:4860:4860::8888 / 2001:4860:4860::8844) [IPv6]
echo 3. Cloudflare DNS (1.1.1.1 / 1.0.0.1) [IPv4] - (2606:4700:4700::1111 / 2606:4700:4700::1001) [IPv6]
echo 4. OpenDNS (208.67.222.222 / 208.67.220.220) [IPv4] - (2620:119:35::35 / 2620:119:53::53) [IPv6]
echo 5. Quad9 DNS (9.9.9.9 / 149.112.112.112) [IPv4] - (2620:fe::fe / 2620:fe::9) [IPv6]
echo 6. Comodo Secure DNS (8.26.56.26 / 8.20.247.20) [IPv4]
echo 7. Verisign DNS (64.6.64.6 / 64.6.65.6) [IPv4]
echo 8. Yandex DNS (77.88.8.8 / 77.88.8.1) [IPv4] - (2a02:6b8::feed:0ff / 2a02:6b8:0:1::feed:0ff) [IPv6]
echo 9. CleanBrowsing DNS (185.228.168.9 / 185.228.169.9) [IPv4] - (2a0d:2a00:1::2 / 2a0d:2a00:2::2) [IPv6]
echo 10. Neustar DNS (156.154.70.1 / 156.154.71.1) [IPv4] - (2610:a1:1018::1 / 2610:a1:1019::1) [IPv6]
echo 11. SafeDNS (195.46.39.39 / 195.46.39.40) [IPv4]
echo 12. OpenNIC DNS (185.121.177.177 / 169.239.202.202) [IPv4]
echo 13. Dyn DNS (216.146.35.35 / 216.146.36.36) [IPv4]
echo 14. Alternate DNS (198.101.242.72 / 23.253.163.53) [IPv4]
echo 15. Close
echo =========================================
set /p option="Select option (1-15): "

if "%option%"=="1" goto CustomDNS
if "%option%"=="2" goto GoogleDNS
if "%option%"=="3" goto CloudflareDNS
if "%option%"=="4" goto OpenDNS
if "%option%"=="5" goto Quad9DNS
if "%option%"=="6" goto ComodoDNS
if "%option%"=="7" goto VerisignDNS
if "%option%"=="8" goto YandexDNS
if "%option%"=="14" goto CleanBrowsingDNS
if "%option%"=="10" goto NeustarDNS
if "%option%"=="11" goto SafeDNS
if "%option%"=="12" goto OpenNICDNS
if "%option%"=="13" goto DynDNS
if "%option%"=="14" goto AlternateDNS
if "%option%"=="15" exit

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

:Quad9DNS
echo Configuring Quad9 DNS (9.9.9.9 / 149.112.112.112) [IPv4] and (2620:fe::fe / 2620:fe::9) [IPv6]...
netsh interface ipv4 set dns name="Ethernet" static 9.9.9.9
netsh interface ipv4 add dns name="Ethernet" 149.112.112.112 index=2
netsh interface ipv6 set dns name="Ethernet" static 2620:fe::fe
netsh interface ipv6 add dns name="Ethernet" 2620:fe::9 index=2
goto End

:ComodoDNS
echo Configuring Comodo Secure DNS (8.26.56.26 / 8.20.247.20) [IPv4]...
netsh interface ipv4 set dns name="Ethernet" static 8.26.56.26
netsh interface ipv4 add dns name="Ethernet" 8.20.247.20 index=2
goto End

:VerisignDNS
echo Configuring Verisign DNS (64.6.64.6 / 64.6.65.6) [IPv4]...
netsh interface ipv4 set dns name="Ethernet" static 64.6.64.6
netsh interface ipv4 add dns name="Ethernet" 64.6.65.6 index=2
goto End

:YandexDNS
echo Configuring Yandex DNS (77.88.8.8 / 77.88.8.1) [IPv4] and (2a02:6b8::feed:0ff / 2a02:6b8:0:1::feed:0ff) [IPv6]...
netsh interface ipv4 set dns name="Ethernet" static 77.88.8.8
netsh interface ipv4 add dns name="Ethernet" 77.88.8.1 index=2
netsh interface ipv6 set dns name="Ethernet" static 2a02:6b8::feed:0ff
netsh interface ipv6 add dns name="Ethernet" 2a02:6b8:0:1::feed:0ff index=2
goto End

:CleanBrowsingDNS
echo Configuring CleanBrowsing DNS (185.228.168.9 / 185.228.169.9) [IPv4] and (2a0d:2a00:1::2 / 2a0d:2a00:2::2) [IPv6]...
netsh interface ipv4 set dns name="Ethernet" static 185.228.168.9
netsh interface ipv4 add dns name="Ethernet" 185.228.169.9 index=2
netsh interface ipv6 set dns name="Ethernet" static 2a0d:2a00:1::2
netsh interface ipv6 add dns name="Ethernet" 2a0d:2a00:2::2 index=2
goto End

:NeustarDNS
echo Configuring Neustar DNS (156.154.70.1 / 156.154.71.1) [IPv4] and (2610:a1:1018::1 / 2610:a1:1019::1) [IPv6]...
netsh interface ipv4 set dns name="Ethernet" static 156.154.70.1
netsh interface ipv4 add dns name="Ethernet" 156.154.71.1 index=2
netsh interface ipv6 set dns name="Ethernet" static 2610:a1:1018::1
netsh interface ipv6 add dns name="Ethernet" 2610:a1:1019::1 index=2
goto End

:SafeDNS
echo Configuring SafeDNS (195.46.39.39 / 195.46.39.40) [IPv4]...
netsh interface ipv4 set dns name="Ethernet" static 195.46.39.39
netsh interface ipv4 add dns name="Ethernet" 195.46.39.40 index=2
goto End

:OpenNICDNS
echo Configuring OpenNIC DNS (185.121.177.177 / 169.239.202.202) [IPv4]...
netsh interface ipv4 set dns name="Ethernet" static 185.121.177.177
netsh interface ipv4 add dns name="Ethernet" 169.239.202.202 index=2
goto End

:DynDNS
echo Configuring Dyn DNS (216.146.35.35 / 216.146.36.36) [IPv4]...
netsh interface ipv4 set dns name="Ethernet" static 216.146.35.35
netsh interface ipv4 add dns name="Ethernet" 216.146.36.36 index=2
goto End

:AlternateDNS
echo Configuring Alternate DNS (198.101.242.72 / 23.253.163.53) [IPv4]...
netsh interface ipv4 set dns name="Ethernet" static 198.101.242.72
netsh interface ipv4 add dns name="Ethernet" 23.253.163.53 index=2
goto End

:End
echo Configuration completed!
echo =========================================
echo Current Network Information:
echo =========================================
powershell -Command "(Get-NetIPConfiguration -InterfaceAlias 'Ethernet')"

echo =========================================
pause
