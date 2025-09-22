
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import json

class ANBIMADebenturesScraper:
    def __init__(self, headless=False):
        self.driver = None
        self.setup_driver(headless)

    def setup_driver(self, headless=False):
        """Configura o driver do Chrome com opções anti-detecção"""
        options = Options()

        # Configurações anti-bot detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # User-Agent personalizado
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Outras configurações
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        if headless:
            options.add_argument("--headless=new")

        # Instala e configura o ChromeDriver automaticamente
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        # Remove a propriedade navigator.webdriver
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def human_delay(self, min_sec=1, max_sec=3):
        """Adiciona delay aleatório para simular comportamento humano"""
        time.sleep(random.uniform(min_sec, max_sec))

    def scroll_page(self, driver):
        """Simula scroll humano na página"""
        # Scroll gradual para baixo
        total_height = driver.execute_script("return document.body.scrollHeight")
        current_position = 0
        scroll_increment = random.randint(300, 500)

        while current_position < total_height:
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            current_position += scroll_increment
            time.sleep(random.uniform(0.5, 1.5))

    def wait_for_page_load(self):
        """Aguarda o carregamento completo da página"""
        wait = WebDriverWait(self.driver, 20)

        # Aguarda que o estado da página seja 'complete'
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

        # Aguarda que não haja requisições AJAX pendentes (se jQuery estiver presente)
        try:
            wait.until(lambda driver: driver.execute_script("return jQuery.active == 0") if driver.execute_script("return typeof jQuery != 'undefined'") else True)
        except:
            pass

    def scrape_debentures(self):
        """Realiza o scraping das debêntures"""
        try:
            # Navega para a página
            print("Navegando para o site da ANBIMA...")
            self.driver.get("https://data.anbima.com.br/busca/debentures")

            # Aguarda carregamento
            self.wait_for_page_load()
            self.human_delay(2, 4)

            # Aguarda elementos específicos carregarem
            wait = WebDriverWait(self.driver, 30)

            # Possíveis seletores para aguardar (adaptar conforme estrutura real)
            try:
                # Aguarda tabela ou lista de debêntures
                debentures_container = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "list-item__container, table, .list-container, .debentures-list, [data-testid*='debenture'], list-item__container, col-xs-12, anbima-ui-dropdown__container, anbima-ui-pagination__dropdown"))
                )
                print("Container de debêntures encontrado!")
            except:
                # Se não encontrar, tenta aguardar qualquer conteúdo dinâmico
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
                print("Página carregada, procurando conteúdo...")

            # Scroll para garantir que todo conteúdo seja carregado
            self.scroll_page(self.driver)
            self.human_delay(2, 3)

            # Extração de dados - seletores genéricos que devem ser adaptados
            debentures_data = []

            # Tenta diferentes estratégias para encontrar os dados
            strategies = [
                "tr",  # Linhas de tabela
                "[data-testid*='debenture']",  # Elementos com data-testid
                ".debenture-item",  # Classes CSS possíveis
                "[class*='debenture']",  # Qualquer classe contendo 'debenture'
            ]

            found_elements = []
            for strategy in strategies:
                elements = self.driver.find_elements(By.CSS_SELECTOR, strategy)
                if elements:
                    found_elements = elements
                    print(f"Encontrados {len(elements)} elementos usando seletor: {strategy}")
                    break

            if not found_elements:
                # Se não encontrar elementos específicos, extrai texto da página
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                print("Texto da página extraído. Tamanho:", len(page_text))
                return {"page_content": page_text}

            # Processa elementos encontrados
            for i, element in enumerate(found_elements[:20]):  # Limita a 20 elementos
                try:
                    # Extrai informações básicas
                    element_data = {
                        "index": i + 1,
                        "text": element.text.strip(),
                        "html": element.get_attribute("outerHTML")[:500]  # Primeiros 500 chars
                    }

                    # Tenta extrair dados específicos se possível
                    sub_elements = element.find_elements(By.CSS_SELECTOR, "td, span, div")
                    if sub_elements:
                        element_data["sub_elements"] = [elem.text.strip() for elem in sub_elements[:10]]

                    debentures_data.append(element_data)

                except Exception as e:
                    print(f"Erro ao processar elemento {i}: {e}")
                    continue

            return debentures_data

        except Exception as e:
            print(f"Erro durante o scraping: {e}")
            return None

    def save_to_csv(self, data, filename="debentures_anbima.csv"):
        """Salva os dados em CSV"""
        if data and isinstance(data, list):
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Dados salvos em {filename}")
            return filename
        else:
            print("Dados inválidos para salvar em CSV")
            return None

    def close(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()

# Exemplo de uso
def main():
    scraper = ANBIMADebenturesScraper(headless=True)  # headless=False para ver o navegador

    try:
        print("Iniciando scraping da ANBIMA...")
        data = scraper.scrape_debentures()

        if data:
            print(f"Dados extraídos: {len(data) if isinstance(data, list) else 1} itens")

            # Salva em CSV se for lista de dados
            if isinstance(data, list):
                filename = scraper.save_to_csv(data)
                print(f"Arquivo salvo: {filename}")

            # Mostra amostra dos dados
            if isinstance(data, list) and data:
                print("\nAmostra dos dados:")
                for item in data[:3]:
                    print(f"- {item}")
            else:
                print("\nConteúdo extraído (primeiros 500 chars):")
                content = str(data)[:500] + "..." if len(str(data)) > 500 else str(data)
                print(content)
        else:
            print("Nenhum dado foi extraído.")

    except Exception as e:
        print(f"Erro na execução: {e}")

    finally:
        scraper.close()

if __name__ == "__main__":
    main()