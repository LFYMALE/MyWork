import scrapy
from bs4 import BeautifulSoup
import json

class MetricsSpider(scrapy.Spider):
    name = 'metrics_spider'
    start_urls = ['http://example.com/metrics']  # Remplace par l'URL de ton API

    def parse(self, response):
        # Parse la réponse HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver toutes les balises <script>
        script_tags = soup.find_all('script')

        for script in script_tags:
            # Vérifie que le contenu de la balise <script> n'est pas None
            if script.string:
                script_content = script.string

                # Vérifie si la clé 'window.gradio_config' est présente dans le contenu
                if 'window.gradio_config' in script_content:
                    # Extraire la partie de la balise <script> contenant 'window.gradio_config'
                    start_index = script_content.find('window.gradio_config')
                    end_index = script_content.find('};', start_index) + 1

                    if start_index != -1 and end_index != -1:
                        gradio_config_content = script_content[start_index:end_index]

                        # Nettoyer et convertir en JSON
                        try:
                            json_content = gradio_config_content.split('=', 1)[-1].strip().rstrip(';')
                            data = json.loads(json_content)

                            # Traiter les données
                            yield {
                                'config': data
                            }
                        except json.JSONDecodeError as e:
                            self.logger.error("Erreur lors du décodage JSON: %s", str(e))
                        except Exception as e:
                            self.logger.error("Erreur lors du traitement des données: %s", str(e))
