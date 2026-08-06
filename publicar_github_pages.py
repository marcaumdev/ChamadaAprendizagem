import os
import sys
import subprocess
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def publicar_no_github():
    """
    Publica e envia automaticamente as alterações do Dashboard para o GitHub Pages.
    Protege arquivos sigilosos conforme o .gitignore e roda o git push automaticamente.
    """
    caminho_repo = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "=" * 70)
    print("   AUTOMATED GITHUB PAGES PUBLICATION (GIT PUSH AUTO)")
    print("=" * 70)

    # 1. Garantir que o .git está inicializado
    git_dir = os.path.join(caminho_repo, ".git")
    if not os.path.exists(git_dir):
        print("[+] Inicializando repositório Git local...")
        try:
            subprocess.run(["git", "init"], cwd=caminho_repo, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=caminho_repo, check=True)
        except Exception as e:
            print(f"[!] Aviso Git init: {e}")

    # Atualiza o URL do remote origin para o novo repositório se necessário
    url_novo_repo = "https://github.com/marcaumdev/ChamadaAprendizagem.git"
    try:
        subprocess.run(["git", "remote", "set-url", "origin", url_novo_repo], cwd=caminho_repo, capture_output=True)
    except Exception:
        pass

    # 2. Executa git add incluindo .nojekyll para evitar falha no build do GitHub Pages
    print("[+] Adicionando arquivos do Dashboard (respeitando o .gitignore de segurança)...")
    try:
        subprocess.run(["git", "add", "index.html", "dashboard/data.json", ".gitignore", ".nojekyll", "README.md", "publicar_github_pages.py"], cwd=caminho_repo, check=True)
    except Exception as e_add:
        print(f"[!] Git add: {e_add}")

    # 3. Cria o commit com a data e hora da atualização
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    msg_commit = f"Auto update dashboard data: {data_atual}"
    try:
        res_commit = subprocess.run(["git", "commit", "-m", msg_commit], cwd=caminho_repo, capture_output=True, text=True, encoding='utf-8')
        if res_commit.returncode == 0:
            print(f"[+] Commit gerado com sucesso: '{msg_commit}'")
        else:
            print("[+] Sem novas alterações para comitar no momento.")
    except Exception as e_commit:
        print(f"[!] Git commit: {e_commit}")

    # 4. Tenta o git push automático se houver um remote origin configurado
    try:
        res_remote = subprocess.run(["git", "remote", "get-url", "origin"], cwd=caminho_repo, capture_output=True, text=True, encoding='utf-8')
        if res_remote.returncode == 0 and res_remote.stdout.strip():
            remote_url = res_remote.stdout.strip()
            print(f"[+] Repositório remoto vinculado: {remote_url}")
            print("[+] Executando UPLOAD AUTOMÁTICO pro GitHub (git push origin main)...")
            res_push = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=caminho_repo, capture_output=True, text=True, encoding='utf-8')
            if res_push.returncode == 0:
                print("\n" + "*" * 70)
                print("  [★] UPLOAD CONCLUÍDO COM SUCESSO NO GITHUB PAGES!")
                print("  [★] O seu Dashboard online já foi atualizado automaticamente!")
                print("*" * 70 + "\n")
                return True
            else:
                print(f"[!] Aviso no git push: {res_push.stderr.strip()}")
        else:
            print("\n" + "*" * 70)
            print(">>> PASSO ÚNICO PARA VINCULAR AO SEU REPOSISÓRIO DO GITHUB:")
            print("Execute o comando abaixo 1 única vez com a URL do seu repositório no GitHub:")
            print("   git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git")
            print("   git push -u origin main")
            print("Após esse comando, toda execução de EXECUTAR_TUDO.bat fará o upload 100% automático!")
            print("*" * 70 + "\n")
    except Exception as e_push:
        print(f"[!] Status da publicação: {e_push}")

    return False

if __name__ == "__main__":
    publicar_no_github()
