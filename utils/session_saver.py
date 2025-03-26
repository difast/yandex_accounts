# utils/session_saver.py
import tarfile
import time
import logging

def save_session(adb_manager, account_id):
    pass
  

  
   # session_dir = f"sessions/{account_id}"
  #  os.makedirs(session_dir, exist_ok=True)
    
    # Поиск всех возможных баз данных
   # dbs = adb_manager.run_adb_command(
    #    "shell su -c 'find / -name \"*.db\" | grep -i yandex'"
   # ).splitlines()
    
    #for db in dbs:
     #   if db:
    #        adb_manager.run_adb_command(f"pull {db} {session_dir}")
    
   # return session_dir if os.listdir(session_dir) else None