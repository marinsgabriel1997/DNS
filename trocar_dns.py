import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import ctypes
from typing import Tuple
import psutil
import socket

DNS_OPTIONS = {
    "Google": ("8.8.8.8", "8.8.4.4", "2001:4860:4860::8888", "2001:4860:4860::8844"),
    "Cloudflare": ("1.1.1.1", "1.0.0.1", "2606:4700:4700::1111", "2606:4700:4700::1001"),
    "OpenDNS": ("208.67.222.222", "208.67.220.220", "2620:119:35::35", "2620:119:53::53")
}

def is_admin() -> bool:
    try:
        admin_status = ctypes.windll.shell32.IsUserAnAdmin()
        print(f"Verificando se o usuário é administrador: {admin_status}")
        return admin_status
    except Exception as e:
        print(f"Erro ao verificar status de administrador: {e}")
        return False

def run_command(command: str) -> Tuple[bool, str]:
    print(f"Executando comando: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(f"Resultado do comando: {result.stdout}, Erro: {result.stderr}")
        return result.returncode == 0, result.stdout
    except subprocess.SubprocessError as e:
        print(f"Erro ao executar comando: {e}")
        return False, str(e)

def listar_adaptadores():
    adaptadores = []
    adaptadores_com_internet = []
    print("Listando adaptadores de rede...")

    for interface, info in psutil.net_if_addrs().items():
        adaptadores.append(interface)
        if interface in psutil.net_if_stats() and psutil.net_if_stats()[interface].isup:
            print(f"Adaptador ativo encontrado: {interface}")
            
            # Obtém o endereço IPv4 da interface
            ipv4_address = None
            for addr in info:
                if addr.family == socket.AF_INET:  # Verifica se é um endereço IPv4
                    ipv4_address = addr.address
                    break
            
            if ipv4_address:
                print(f"Verificando conectividade da interface {interface} com IP {ipv4_address}...")
                try:
                    # Realiza um ping forçando o uso do IP da interface
                    comando = f'ping -n 1 -S {ipv4_address} 8.8.8.8'
                    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=2)
                    
                    # Verifica se o ping foi bem-sucedido
                    if "Resposta" in resultado.stdout:
                        adaptadores_com_internet.append(interface)
                        print(f"Adaptador {interface} tem conectividade com a internet.")
                    else:
                        print(f"Adaptador {interface} não tem conectividade com a internet.")
                except subprocess.TimeoutExpired:
                    print(f"Adaptador {interface} não tem conectividade com a internet (timeout).")
                except Exception as e:
                    print(f"Erro ao verificar conectividade da interface {interface}: {e}")
            else:
                print(f"Adaptador {interface} não tem um endereço IPv4 configurado.")
        else:
            print(f"Adaptador {interface} está inativo.")

    return [f"{'* ' if nome in adaptadores_com_internet else ''}{nome}" for nome in adaptadores]


def formatar_saida(texto: str) -> str:
    linhas = texto.splitlines()
    saida_formatada = []
    
    for i, linha in enumerate(linhas):
        linha = ' '.join(linha.strip().split())  # Remove espaços extras
        
        if i == 0:
            saida_formatada.append(linha)  # Primeira linha sem tabulação
        elif ":" in linha:
            chave, valor = linha.split(":", 1)
            saida_formatada.append(f"  {chave}:")  # Chave recebe um tab
            saida_formatada.append(f"    {valor.strip()}")  # Valor recebe dois tabs
        else:
            saida_formatada.append(f"    {linha}")  # Linhas sem ':' recebem dois tabs
    
    return "\n".join(saida_formatada)

def obter_propriedades_adaptador(adaptador: str) -> str:
    print(f"Obtendo propriedades do adaptador: {adaptador}")
    propriedades_text.delete(1.0, tk.END)
    propriedades_text.insert(tk.END, "Obtendo propriedades do adaptador, por favor aguarde...")
    root.update()
    comando = f'powershell Get-NetIPConfiguration -InterfaceAlias "{adaptador}" -Detailed'
    
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if resultado.returncode == 0:
            return resultado.stdout.strip()
        else:
            return "Erro ao obter propriedades."
    
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return "Erro ao obter propriedades."

def atualizar_propriedades():
    adaptador = adaptador_var.get().replace("* ", "")
    print(f"Atualizando propriedades para o adaptador: {adaptador}")
    if adaptador:
        propriedades = obter_propriedades_adaptador(adaptador)
        propriedades_text.delete(1.0, tk.END)  # Limpa o texto anterior
        if propriedades:  # Verifica se há propriedades para inserir            
            propriedades_text.insert(tk.END, propriedades)  # Insere as novas propriedades
        else:
            print("Nenhuma propriedade encontrada.")
            propriedades_text.insert(tk.END, "Nenhuma propriedade encontrada.")  # Mensagem padrão se não houver propriedades
    else:
        propriedades_text.delete(1.0, tk.END)  # Limpa o texto se nenhum adaptador for selecionado

def restaurar_dns():
    if not is_admin():
        messagebox.showerror("Erro", "Necessário executar como administrador!")
        return

    adaptador = adaptador_var.get().replace("* ", "")
    print(f"Restaurando DNS para o adaptador: {adaptador}")
    if not adaptador:
        messagebox.showerror("Erro", "Selecione um adaptador")
        return

    try:
        comandos = [
            f'netsh interface ip set dns "{adaptador}" dhcp',
            f'netsh interface ipv6 set dns "{adaptador}" dhcp'
        ]

        for cmd in comandos:
            sucesso, erro = run_command(cmd)
            if not sucesso:
                raise Exception(f"Erro ao executar comando: {erro}")

        messagebox.showinfo("Sucesso", "DNS restaurado para DHCP")
        atualizar_propriedades()
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        print(f"Erro ao restaurar DNS: {e}")

def aplicar_dns():
    if not is_admin():
        messagebox.showerror("Erro", "Necessário executar como administrador!")
        return

    adaptador = adaptador_var.get().replace("* ", "")
    print(f"Aplicando DNS para o adaptador: {adaptador}")
    if not adaptador:
        messagebox.showerror("Erro", "Selecione um adaptador")
        return

    dns1 = dns1_var.get()
    dns2 = dns2_var.get()
    print(f"DNS Primário: {dns1}, DNS Secundário: {dns2}")

    if messagebox.askyesno("Confirmar", "Deseja aplicar as alterações de DNS?"):
        try:
            progress_window = tk.Toplevel(root)
            progress_window.title("Aplicando DNS")
            progress = ttk.Progressbar(progress_window, length=200, mode='indeterminate')
            progress.pack(padx=20, pady=20)
            progress.start()

            if ipv4_var.get():
                print("Aplicando configurações de DNS para IPv4...")
                if dns1 == dns2:
                    ipv4_primario = DNS_OPTIONS[dns1][0]
                    ipv4_secundario = DNS_OPTIONS[dns1][1]
                else:
                    ipv4_primario = DNS_OPTIONS[dns1][0]
                    ipv4_secundario = DNS_OPTIONS[dns2][0]

                comandos_ipv4 = [
                    f'netsh interface ip set dns name="{adaptador}" static {ipv4_primario}',
                    f'netsh interface ip add dns name="{adaptador}" {ipv4_secundario} index=2'
                ]

                for cmd in comandos_ipv4:
                    sucesso, erro = run_command(cmd)
                    if not sucesso:
                        raise Exception(f"Erro IPv4: {erro}")

            if ipv6_var.get():
                print("Aplicando configurações de DNS para IPv6...")
                if dns1 == dns2:
                    ipv6_primario = DNS_OPTIONS[dns1][2]
                    ipv6_secundario = DNS_OPTIONS[dns1][3]
                else:
                    ipv6_primario = DNS_OPTIONS[dns1][2]
                    ipv6_secundario = DNS_OPTIONS[dns2][2]

                comandos_ipv6 = [
                    f'netsh interface ipv6 set dns name="{adaptador}" static {ipv6_primario}',
                    f'netsh interface ipv6 add dns name="{adaptador}" {ipv6_secundario} index=2'
                ]

                for cmd in comandos_ipv6:
                    sucesso, erro = run_command(cmd)
                    if not sucesso:
                        raise Exception(f"Erro IPv6: {erro}")

            progress_window.destroy()
            messagebox.showinfo("Sucesso", "DNS alterado com sucesso!")
            atualizar_propriedades()

        except Exception as e:
            progress_window.destroy()
            messagebox.showerror("Erro", str(e))
            print(f"Erro ao aplicar DNS: {e}")

# Interface gráfica
root = tk.Tk()
root.title("Trocar DNS")
root.geometry("1280x720")  # Altera o tamanho da janela

# Cria um frame para as configurações
config_frame = tk.Frame(root)
config_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

# Cria um frame para o widget de texto
text_frame = tk.Frame(root)
text_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Componentes da interface (configurações)
tk.Label(config_frame, text="Selecione o Adaptador de Rede:").pack(pady=5)
adaptador_var = tk.StringVar(value="")
adaptadores_lista = listar_adaptadores()
adaptador_dropdown = ttk.Combobox(config_frame, textvariable=adaptador_var, values=adaptadores_lista, state="readonly")
adaptador_dropdown.pack(pady=5)

tk.Label(config_frame, text="DNS Primário:").pack(pady=5)
dns1_var = tk.StringVar(value="")
dns1_dropdown = ttk.Combobox(config_frame, textvariable=dns1_var, values=list(DNS_OPTIONS.keys()), state="readonly")
dns1_dropdown.pack(pady=5)

tk.Label(config_frame, text="DNS Secundário:").pack(pady=5)
dns2_var = tk.StringVar(value="")
dns2_dropdown = ttk.Combobox(config_frame, textvariable=dns2_var, values=list(DNS_OPTIONS.keys()), state="readonly")
dns2_dropdown.pack(pady=5)

ipv4_var = tk.BooleanVar(value=False)
ipv6_var = tk.BooleanVar(value=False)

ipv4_checkbox = tk.Checkbutton(config_frame, text="Aplicar DNS para IPv4", variable=ipv4_var)
ipv4_checkbox.pack(pady=5)

ipv6_checkbox = tk.Checkbutton(config_frame, text="Aplicar DNS para IPv6", variable=ipv6_var)
ipv6_checkbox.pack(pady=5)

botoes_frame = tk.Frame(config_frame)
botoes_frame.pack(pady=15)

tk.Button(botoes_frame, text="Aplicar DNS", command=aplicar_dns, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(botoes_frame, text="Restaurar DNS (DHCP)", command=restaurar_dns, bg="blue", fg="white").pack(side=tk.LEFT, padx=5)

# Adiciona um rótulo para mostrar as propriedades do adaptador
tk.Label(config_frame, text="Propriedades do Adaptador:").pack(pady=5)
propriedades_text = tk.Text(text_frame, height=40, width=80)  # Ajuste a altura e largura conforme necessário
propriedades_text.pack(pady=5, fill=tk.BOTH, expand=True)

# Atualiza as propriedades quando um adaptador é selecionado
adaptador_var.trace("w", lambda *args: atualizar_propriedades())

root.mainloop()
