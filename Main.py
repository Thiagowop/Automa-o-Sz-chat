#Código de automaçäo monitoramento de clientes

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

def inicializar_driver():
    return webdriver.Chrome()

#Executa as operações de login.
def login(driver):

    driver.get("https://colchoesortobom.sz.chat/static/signin")

    wait = WebDriverWait(driver, 10)
    campo_email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
    campo_email.send_keys("Email")

    campo_senha = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
    campo_senha.send_keys("Senha")

    botao_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    botao_login.click()

    print("Login realizado com sucesso. Monitorando novos clientes.")

#Envia uma mensagem automática para o cliente
def enviar_mensagem(driver):
    
    try:
        # Aguarda o campo de mensagem estar presente
        wait = WebDriverWait(driver, 10)
        campo_mensagem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='message']")))
        
        # Digita a mensagem no campo
        mensagem = "Olá! Em breve, um de nossos consultores irá atendê-lo. Por favor, aguarde um momento."
        campo_mensagem.send_keys(mensagem)
        
        # Aguarda o botão de enviar estar clicável e o clica
        botao_enviar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        botao_enviar.click()

        print("Mensagem enviada para o cliente.")

    except TimeoutException:
        print("Campo de mensagem ou botão de envio não encontrado.")
    except ElementClickInterceptedException as e:
        print(f"Erro ao clicar no botão de envio: {e}")

#Verifica novos clientes
def verificar_novos_clientes(driver):
   
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#page-header")))

        try:
            elemento_cliente_novo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-c4f964b0].contact.active")))
        except TimeoutException:
            elemento_cliente_novo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-c4f964b0].contact")))

        elemento_cliente_novo.click()
        print("Cliente em atendimento encontrado! Clicando para iniciar.")

       
        time.sleep(2)  
        enviar_mensagem(driver)

    except TimeoutException:
        print("Elemento do cliente não encontrado.")
    except ElementClickInterceptedException as e:
        print(f"Erro ao clicar em novo cliente: {e}")
    except NoSuchElementException as e:
        print(f"Elemento não encontrado: {e}")

def principal():
    driver = inicializar_driver()
    try:
        login(driver)

        while True:
            try:
                verificar_novos_clientes(driver)
            except (ElementClickInterceptedException, NoSuchElementException) as e:
                print(f"Erro ao clicar em novo cliente ou elemento não encontrado: {e}. Reiniciando...")
                driver.quit()
                driver = inicializar_driver()
                login(driver)
            except Exception as e:
                print(f"Erro inesperado: {e}. Reiniciando...")
                driver.quit()
                driver = inicializar_driver()
                login(driver)
            time.sleep(5)  

    finally:
        driver.quit()

if __name__ == "__main__":
    principal()
