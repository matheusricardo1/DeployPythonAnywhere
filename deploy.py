import requests
import os

class PythonAnywhereAPI:
    def __init__(self, username, api_token, project_path):
        self.username = username
        self.api_token = api_token
        self.project_path = project_path
        self.domain_name = f"{username}.pythonanywhere.com"
        self.base_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/"
        self.headers = {'Authorization': f'Token {api_token}'}

        if not self.api_token:
            raise ValueError("Erro: Por favor, defina a variável de ambiente PA_API_TOKEN ou adicione-a ao seu arquivo .env com o seu token de API do PythonAnywhere.")

    def list_consoles(self):
        """Lista os consoles existentes."""
        response = requests.get(self.base_url + 'consoles/', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Falha ao listar consoles: {response.status_code}")
            print(response.text)
            return []

    def get_active_console(self):
        """Obtém um console bash."""
        consoles = self.list_consoles()
        for console in consoles:
            console_id = console['id']
            executable = console.get('executable', '').lower()
            print(f"Verificando console ID {console_id}: executable={executable}")
            if 'bash' in executable:
                print(f"Usando o console com ID: {console_id}")
                return console_id
        print("Nenhum console bash encontrado.")
        return None

    def send_command(self, console_id, command):
        """Envia um comando para o console."""
        data = {'input': command + '\n'}
        response = requests.post(self.base_url + f'consoles/{console_id}/send_input/', headers=self.headers, data=data)
        if response.status_code == 200:
            print(f"Comando \"{command}\" enviado com sucesso.")
            return True
        else:
            print(response.text)
            raise Exception(f"Falha ao enviar o comando \"{command}\" para o console {console_id}: {response.status_code}")

    def reload_webapp(self):
        """Recarrega o aplicativo web no PythonAnywhere."""
        response = requests.post(self.base_url + f'webapps/{self.domain_name}/reload/', headers=self.headers)
        if response.status_code == 200:
            print(f"O web app https://{self.domain_name} foi recarregado com sucesso.")
        else:
            print(f"Falha ao recarregar o web app: {response.status_code}")
            print(response.text)

    def deploy(self):
        """Executa o processo de deploy."""
        console_id = self.get_active_console()
        if not console_id:
            print("Por favor, abra um console bash no PythonAnywhere e tente novamente.")
            return

        project_directory = f"/home/{self.username}/{self.project_path}"
        self.send_command(console_id, f"cd {project_directory}")
        self.send_command(console_id, "git stash")
        self.send_command(console_id, "git pull")

        self.reload_webapp()

if __name__ == '__main__':
    USERNAME = 'matheusstore'
    API_TOKEN = os.environ.get('PA_API_TOKEN')
    PROJECT_PATH = 'DeployPythonAnywhere'

    try:
        pa_api = PythonAnywhereAPI(USERNAME, API_TOKEN, PROJECT_PATH)
        pa_api.deploy()
    except ValueError as e:
        print(e)
