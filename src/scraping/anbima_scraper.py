
"""
Exemplo simples de web scraper para ANBIMA usando Selenium
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def criar_driver():
    """Cria e configura o driver Chrome"""
    options = Options()

    # Configurações para evitar detecção de bot
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Configurações adicionais
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Para executar em modo invisível (opcional)
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    # Remove a propriedade que identifica automação
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

def scraping_anbima_debentures():
    """Função principal de scraping"""
    driver = criar_driver()

    try:
        print("Acessando site da ANBIMA...")
        driver.get("https://data.anbima.com.br/busca/debentures")

        # Aguarda o carregamento da página (até 30 segundos)
        wait = WebDriverWait(driver, 30)

        # Aguarda que a página esteja completamente carregada
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        print("Página carregada, aguardando elementos...")
        time.sleep(5)  # Aguarda elementos dinâmicos

        # Tenta encontrar elementos da página
        # NOTA: Estes seletores devem ser ajustados baseado na estrutura real da página
        possible_selectors = [
            "list-item__container"
        ]

        elements_found = []
        for selector in possible_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Encontrados {len(elements)} elementos com seletor: {selector}")
                    elements_found = elements
                    break
            except Exception as e:
                continue

        if not elements_found:
            print("Nenhum elemento específico encontrado, extraindo conteúdo geral...")
            # Extrai todo o texto da página
            body = driver.find_element(By.TAG_NAME, "body")
            content = body.text
            print(f"Conteúdo extraído: {len(content)} caracteres")
            return content

        # Processa os elementos encontrados
        dados_extraidos = []
        print(f"Processando {len(elements_found)} elementos...")

        for i, element in enumerate(elements_found[:10]):  # Limita aos primeiros 10
            try:
                texto = element.text.strip()
                if texto:  # Só adiciona se tiver conteúdo
                    dados_extraidos.append({
                        'indice': i + 1,
                        'conteudo': texto,
                        'html_sample': element.get_attribute('outerHTML')[:200]  # Amostra do HTML
                    })
            except:
                continue

        return dados_extraidos

    except Exception as e:
        print(f"Erro durante o scraping: {e}")
        return None

    finally:
        driver.quit()

def salvar_em_csv(dados, arquivo="anbima_debentures.csv"):
    """Salva os dados em arquivo CSV"""
    if not dados:
        print("Nenhum dado para salvar")
        return

    if isinstance(dados, str):
        # Se for string, salva como texto simples
        with open("anbima_content.txt", "w", encoding="utf-8") as f:
            f.write(dados)
        print("Conteúdo salvo em anbima_content.txt")
    else:
        # Se for lista, salva como CSV
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            if dados:
                writer = csv.DictWriter(f, fieldnames=dados[0].keys())
                writer.writeheader()
                writer.writerows(dados)
        print(f"Dados salvos em {arquivo}")

if __name__ == "__main__":
    # Executa o scraping
    dados = scraping_anbima_debentures()

    if dados:
        print(f"Scraping concluído! Dados extraídos.")
        salvar_em_csv(dados)
    else:
        print("Nenhum dado foi extraído.")