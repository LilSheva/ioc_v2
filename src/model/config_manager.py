import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent.parent / "config.txt"

class ConfigManager:
    def __init__(self):
        self.config_data = self.load()
    def load(self):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._create_default()
    def save(self):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f: json.dump(self.config_data, f, indent=4, ensure_ascii=False)
        except IOError as e: print(f"Ошибка при сохранении файла конфигурации: {e}")
    def get_ioc_types(self):
        return self.config_data.get("ioc_types", {})
    def update_ioc_types(self, new_ioc_types_data):
        self.config_data["ioc_types"] = new_ioc_types_data
    def _create_default(self):
        default_config = {
            "ioc_types": {
                "IP": {"enabled": True, "regex": "\\b(?:\\d{1,3}(?:\\[\\.\\]|\\.)){3}\\d{1,3}\\b", "report_template": {"Тип Индикатора": "IP-адрес", "Статус Активности NTA": "", "Статус Активности SIEM (MP)": ""}, "query_templates": {"MP10": ["src.ip = \"{ioc}\"", "dst.ip = \"{ioc}\""], "NAD": ["src.ip == \"{ioc}\"", "dst.ip == \"{ioc}\"", "host.ip == \"{ioc}\""]}},
                "DNS": {"enabled": True, "regex": "\\b(?=.*[a-zA-Z])[\\w.-]+\\[\\.\\][\\w.-]+\\b", "report_template": {"Тип Индикатора": "Домен", "Статус Активности NTA": "", "Статус Активности SIEM (MP)": "---------------"}, "query_templates": {"MP10": ["event_src.fqdn = \"{ioc}\""], "NAD": ["src.dns ~ \"{ioc}\""]}},
                "URI": {"enabled": True, "priority": 3, "regex": "[a-zA-Z]+\\[:\\]//[\\w\\d\\.\\[\\]\\-:%/\\?=&#]+[\\w\\d/]", "report_template": {"Тип Индикатора": "URI"}, "query_templates": {"MP10": ["object.url = \"{ioc}\""], "NAD": ["http.rqs.url ~ \"{ioc}\""]}},
                "SHA256": {"enabled": True, "regex": "\\b[a-fA-F0-9]{64}\\b", "report_template": {"Тип Индикатора": "SHA256", "Статус Активности NTA": "---------------", "Статус Активности SIEM (MP)": ""}, "query_templates": {"MP10": ["object.hash.sha256 = \"{ioc}\""], "NAD": []}},
                "SHA1": {"enabled": True, "regex": "\\b[a-fA-F0-9]{40}\\b", "report_template": {"Тип Индикатора": "SHA1", "Статус Активности NTA": "", "Статус Активности SIEM (MP)": ""}, "query_templates": {"MP10": ["object.hash.sha1 = \"{ioc}\""], "NAD": []}},
                "MD5": {"enabled": True, "regex": "\\b[a-fA-F0-9]{32}\\b", "report_template": {"Тип Индикатора": "MD5", "Статус Активности NTA": "", "Статус Активности SIEM (MP)": ""}, "query_templates": {"MP10": ["object.hash.md5 = \"{ioc}\""], "NAD": ["files.md5 == \"{ioc}\""]}},
                "File": {"enabled": True, "regex": "\"(?P<value>[^\\\"]+\\.\\w+(?:\\.\\w+)*)\"", "report_template": {"Тип Индикатора": "File", "Статус Активности NTA": "", "Статус Активности SIEM (MP)": ""}, "query_templates": {"MP10": ["object.name CONTAINS \"{ioc}\""], "NAD": ["files.filename ~ \"{ioc}\""]}},
                "Email": {"enabled": True, "regex": "\\b[\\w\\.-]+@[\\w\\.-]+\\[\\.\\][\\w\\.-]+\\b", "report_template": {"Тип Индикатора": "Email", "Статус Активности NTA": "", "Статус Активности SIEM (MP)": ""}, "query_templates": {"MP10": ["subject.account.contact CONTAINS \"{ioc}\""], "NAD": ["mail.from == \"{ioc}\""]}},
                "Registry": {"enabled": True, "regex": "(?i)(?:HKEY_LOCAL_MACHINE|HKLM|HKEY_CURRENT_USER|HKCU)\\\\[\\\\\\w\\s\\.-]+?(?=\\s|\\.|,|$|\")", "report_template": {"Тип Индикатора": "Ключ реестра", "Статус Активности NTA": "", "Статус Активности SIEM (MP)": ""}, "query_templates": {"MP10": ["object.path = \"{ioc}\""], "NAD": []}}
            }
        }
        self.config_data = default_config
        self.save()
        return self.config_data