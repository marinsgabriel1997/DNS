import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import ctypes
from typing import Tuple, Optional

DNS_OPTIONS = {
    "Google": ("8.8.8.8", "8.8.4.4", "2001:4860:4860::8888", "2001:4860:4860::8844"),
    "Cloudflare": ("1.1.1.1", "1.0.0.1", "2606:4700:4700::1111", "2606:4700:4700::1001"),
    "OpenDNS": ("208.67.222.222", "208.67.220.220", "2620:119:35::35", "2620:119:53::53")
}

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(command: str) -> Tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stderr
    except subprocess.SubprocessError as e:
        return False, str(e)

def listar_adaptadores():
    adaptadores = []
    adaptadores_ativos = []

    try:
        # Executa o comando para listar os adaptadores de rede
        resultado = subprocess.run("chcp 65001 > nul & netsh interface show interface", shell=True, capture_output=True, text=True, encoding="utf-8")

        # Expressão regular para encontrar os adaptadores
        linhas = resultado.stdout.split("\n")
        for linha in linhas[3:]:  # Ignora as três primeiras linhas do cabeçalho
            partes = re.split(r"\s{2,}", linha.strip())
            if len(partes) >= 4:
                status, _, _, nome = partes
                adaptadores.append(nome)
                if status.lower() == "enabled":
                    adaptadores_ativos.append(nome)  # Marca os adaptadores ativos

        # Adiciona "*" às interfaces ativas
        return [f"{'* ' if nome in adaptadores_ativos else ''}{nome}" for nome in adaptadores]
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar adaptadores: {e}")
        return []
def restaurar_dns():
    if not is_admin():
        messagebox.showerror("Erro", "Necessário executar como administrador!")
        return

    adaptador = adaptador_var.get().replace("* ", "")
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
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def aplicar_dns():
    if not is_admin():
        messagebox.showerror("Erro", "Necessário executar como administrador!")
        return

    adaptador = adaptador_var.get().replace("* ", "")
    if not adaptador:
        messagebox.showerror("Erro", "Selecione um adaptador")
        return

    dns1 = dns1_var.get()
    dns2 = dns2_var.get()
    
    if messagebox.askyesno("Confirmar", "Deseja aplicar as alterações de DNS?"):
        try:
            progress_window = tk.Toplevel(root)
            progress_window.title("Aplicando DNS")
            progress = ttk.Progressbar(progress_window, length=200, mode='indeterminate')
            progress.pack(padx=20, pady=20)
            progress.start()
            
            if ipv4_var.get():
                if dns1 == dns2:
                    ipv4_primario = DNS_OPTIONS[dns1][0]
                    ipv4_secundario = DNS_OPTIONS[dns1][1]  # Usar o segundo IP do mesmo provedor
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
                if dns1 == dns2:
                    ipv6_primario = DNS_OPTIONS[dns1][2]
                    ipv6_secundario = DNS_OPTIONS[dns1][3]  # Usar o quarto IP do mesmo provedor
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
            
        except Exception as e:
            progress_window.destroy()
            messagebox.showerror("Erro", str(e))

# Interface gráfica
root = tk.Tk()
root.title("Trocar DNS")
root.geometry("400x400")

# Componentes da interface
tk.Label(root, text="Selecione o Adaptador de Rede:").pack(pady=5)
adaptador_var = tk.StringVar()
adaptadores_lista = listar_adaptadores()
adaptador_dropdown = ttk.Combobox(root, textvariable=adaptador_var, values=adaptadores_lista, state="readonly")
adaptador_dropdown.pack(pady=5)

for i, adaptador in enumerate(adaptadores_lista):
    if adaptador.startswith("* "):
        adaptador_dropdown.current(i)
        break

tk.Label(root, text="DNS Primário:").pack(pady=5)
dns1_var = tk.StringVar(value="Google")
dns1_dropdown = ttk.Combobox(root, textvariable=dns1_var, values=list(DNS_OPTIONS.keys()), state="readonly")
dns1_dropdown.pack(pady=5)

tk.Label(root, text="DNS Secundário:").pack(pady=5)
dns2_var = tk.StringVar(value="Cloudflare")
dns2_dropdown = ttk.Combobox(root, textvariable=dns2_var, values=list(DNS_OPTIONS.keys()), state="readonly")
dns2_dropdown.pack(pady=5)

ipv4_var = tk.BooleanVar(value=True)
ipv6_var = tk.BooleanVar(value=True)

ipv4_checkbox = tk.Checkbutton(root, text="Aplicar DNS para IPv4", variable=ipv4_var)
ipv4_checkbox.pack(pady=5)

ipv6_checkbox = tk.Checkbutton(root, text="Aplicar DNS para IPv6", variable=ipv6_var)
ipv6_checkbox.pack(pady=5)

botoes_frame = tk.Frame(root)
botoes_frame.pack(pady=15)

tk.Button(botoes_frame, text="Aplicar DNS", command=aplicar_dns, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(botoes_frame, text="Restaurar DNS", command=restaurar_dns, bg="orange", fg="white").pack(side=tk.LEFT, padx=5)

root.mainloop()
