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



filter {
  # Si le contenu de `message` est un JSON, utilisez le filtre JSON
  json {
    source => "message"  # Assurez-vous que `message` est le champ contenant le JSON
  }

  # Extraire la clé `window.gradio_config` du JSON
  # Assurez-vous que le JSON est correctement imbriqué
  mutate {
    add_field => {
      "gradio_config" => "%{[window][gradio_config]}"
    }
  }

  # Utiliser grok si la clé `window.gradio_config` contient des données non JSON ou nécessite un format spécifique
  # Exemple de grok pour un format de données particulier dans `gradio_config`
  # Remplacez `%{GREEDYDATA:gradio_config_data}` par un modèle approprié selon le format de vos données
  grok {
    match => { "gradio_config" => "%{GREEDYDATA:gradio_config_data}" }
    # Vous pouvez ajouter des options spécifiques de grok si nécessaire
  }
  
  # Si `gradio_config` contient des champs spécifiques à extraire
  # Utilisez des filtres JSON supplémentaires si les données sont imbriquées
  json {
    source => "gradio_config"
    target => "gradio_config_details"
    # Ceci convertira `gradio_config` en un champ structuré `gradio_config_details`
  }
}
