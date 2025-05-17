from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import json
import time 
from service.company import companyService
from service.shares import sharesService
from models.shares import Shares
from decimal import Decimal
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class Scraper:
    def __init__(self):
        self.sharesService = sharesService()
        self.companyService = companyService()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

        self.driver = webdriver.Remote(
            command_executor=os.environ.get("SELENIUM_URL"),
            options=chrome_options
        )

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                """
            },
        )
    
    async def run(self):
        companies = await self.companyService.getAll()
        file_path = os.path.join(os.path.dirname(__file__), "../data/xpaths.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
            
            if(len(companies) == 0):
                print("No companies found")
                return
            
            for company in companies:
                try:
                    self.driver.get(raw_data['url'] + "/" + company.code)
                    xpaths = raw_data['xpaths']   
                    self.driver.find_element("xpath", xpaths["currentQuote"])
                    logger.info(company)    
     
                    try:
                        share = Shares(
                            companyCode = company.code,
                            currentQuote = self.replace_comma(self.driver.find_element("xpath", xpaths["currentQuote"]).text),
                            max52Week=self.replace_comma(self.driver.find_element("xpath", xpaths["max52Week"]).text),
                            min52Week=self.replace_comma(self.driver.find_element("xpath", xpaths["min52Week"]).text),
                            dividendYield=self.replace_comma(self.driver.find_element("xpath", xpaths["dividendYield"]).text),
                            LPA=self.replace_comma(self.driver.find_element("xpath", xpaths["LPA"]).text),
                            VPA=self.replace_comma(self.driver.find_element("xpath", xpaths["VPA"]).text),
                            averageLiquidity=self.replace_comma(self.driver.find_element("xpath", xpaths["averageLiquidity"]).text),
                            market_options=self.replace_comma(self.driver.find_element("xpath", xpaths["market_options"]).text),
                            naturalLiquidityRisk="",
                            NLT="-",
                            LTI="-",
                        )
                        
                        if company.fitch_url:
                            self.driver.get(company.fitch_url)
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths["NLT"])))
                            try:
                                share.NLT = self.driver.find_element("xpath", xpaths["NLT"]).text
                            except Exception as e:
                                logger.info(f"Erro ao obter NLT para {company.code}")                                 
                            try:
                                share.LTI =  self.driver.find_element("xpath", xpaths["LTI"]).text
                            except Exception as e:
                                logger.info(f"Erro ao obter LTI para {company.code}")
                                
                        
                        await self.sharesService.create(share)

                    except Exception as e:
                        logger.warning(f"Erro ao Criar Classe {company.code}:{e}")
                        
                except Exception as e:
                    logger.warning(f"Erro ao processar empresa {company.code}")
                
            logger.info(f"Empresas Processadas com sucesso")
            self.driver.quit()
            

    def replace_comma(self, value: str) -> float:
        cleaned = re.sub(r'[^\d,]', '', value)
        if not re.search(r'\d', cleaned):
            return 0.0

        normalized = cleaned.replace(',', '.')
        try:
            return float(normalized)
        except ValueError:
            return 0.0
        
            
            
        