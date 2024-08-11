import wmi
import platform
import getpass
import socket
import re
import uuid
from psutil import virtual_memory
import logging
import os
from colorama import Fore, Style, init
from tabulate import tabulate

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Инициализация colorama
init(autoreset=True)

LOGO = f"""{Fore.LIGHTRED_EX}
   _____             _____           _                 _____        __      
  / ____|           / ____|         | |               |_   _|      / _|     
 | |  __  ___ _ __ | (___  _   _ ___| |_ ___ _ __ ___   | |  _ __ | |_ ___  
 | | |_ |/ _ \ '_ \ \___ \| | | / __| __/ _ \ '_ ` _ \  | | | '_ \|  _/ _ \ 
 | |__| |  __/ | | |____) | |_| \__ \ ||  __/ | | | | |_| |_| | | | || (_) |
  \_____|\___|_| |_|_____/ \__, |___/\__\___|_| |_| |_|_____|_| |_|_| \___/ 
                            __/ |                                           
                           |___/                                            
{Style.RESET_ALL}
"""

INSTRUCTIONS = f"""
{Fore.LIGHTYELLOW_EX}╭────────────────────━━━━━━━━━━━━━━━━━━━━━────────────────╮
| {Fore.LIGHTGREEN_EX}Используйте » python {os.path.basename(__file__)} {Fore.LIGHTYELLOW_EX}                  |
| {Fore.LIGHTGREEN_EX}Эта программа собирает и отображает информацию о системе{Fore.LIGHTYELLOW_EX}|
| {Fore.LIGHTGREEN_EX}Пример: python {os.path.basename(__file__)}{Fore.LIGHTYELLOW_EX}                         |
╰────────────────────━━━━━━━━━━━━━━━━━━━━━────────────────╯
"""

def get_os_info():
    return f"{Fore.LIGHTCYAN_EX}Операционная система{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}{platform.system()} {platform.release()} [{platform.version()}]{Style.RESET_ALL}"

def get_platform_info():
    return f"{Fore.LIGHTCYAN_EX}Платформа{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}{platform.machine()}{Style.RESET_ALL}"

def get_user_info():
    return f"{Fore.LIGHTCYAN_EX}Имя ПК{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}{getpass.getuser()}{Style.RESET_ALL}"

def get_ip_info():
    return f"{Fore.LIGHTCYAN_EX}IP{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}{socket.gethostbyname(socket.gethostname())}{Style.RESET_ALL}"

def get_mac_info():
    return f"{Fore.LIGHTCYAN_EX}MAC{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}{':'.join(re.findall('..', '%012x' % uuid.getnode()))}{Style.RESET_ALL}"

def get_gpu_info(computer):
    try:
        return f"{Fore.LIGHTCYAN_EX}Видеокарта{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}{computer.Win32_VideoController()[0].Name}{Style.RESET_ALL}"
    except IndexError:
        return f"{Fore.LIGHTCYAN_EX}Видеокарта{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}Информация недоступна{Style.RESET_ALL}"

def get_cpu_info(computer):
    try:
        return f"{Fore.LIGHTCYAN_EX}Процессор{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}{computer.Win32_Processor()[0].Name}{Style.RESET_ALL}"
    except IndexError:
        return f"{Fore.LIGHTCYAN_EX}Процессор{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}Информация недоступна{Style.RESET_ALL}"

def get_ram_info():
    return f"{Fore.LIGHTCYAN_EX}Объем оперативной памяти{Style.RESET_ALL}", f"{Fore.LIGHTMAGENTA_EX}{round(virtual_memory().total / (1024.0 ** 3))} GB{Style.RESET_ALL}"

def gather_system_info():
    computer = wmi.WMI()
    
    # Сбор информации о системе
    info_functions = [
        get_os_info,
        get_platform_info,
        get_user_info,
        get_ip_info,
        get_mac_info,
        lambda: get_gpu_info(computer),
        lambda: get_cpu_info(computer),
        get_ram_info
    ]
    
    # Получение информации и добавление в список
    system_info = [func() for func in info_functions]
    
    # Форматирование заголовков
    headers = [f"{Fore.LIGHTCYAN_EX}Параметр{Style.RESET_ALL}", f"{Fore.LIGHTCYAN_EX}Значение{Style.RESET_ALL}"]
    
    # Вывод информации в виде таблицы
    table = tabulate(system_info, headers=headers, tablefmt="grid")
    logging.info(f"\n{table}")

if __name__ == "__main__":
    # Вывод логотипа и инструкций
    print(LOGO)
    print(INSTRUCTIONS)
    gather_system_info()
