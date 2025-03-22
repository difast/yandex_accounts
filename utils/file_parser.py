# utils/file_parser.py
def parse_logpass(file_path):
    accounts = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) != 5:
                print(f"Ошибка формата строки: {line}")
                continue
            accounts.append({
                "login": parts[0],
                "password": parts[1],
                "proxy_ip": parts[2],
                "proxy_port": parts[3],
                "2fa_code": parts[4]
            })
    return accounts