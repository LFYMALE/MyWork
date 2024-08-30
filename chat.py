from gradio_client import Client
import json
import os


def setup_logging(log_file_path):
    # Assurez-vous que le répertoire du fichier log existe
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)


def log_to_json(log_file_path, log_entry):
    # Enregistrer les logs dans le fichier JSON
    with open(log_file_path, 'a') as f:
        json.dump(log_entry, f)
        f.write('\n')  # Ajouter une nouvelle ligne pour chaque entrée JSON


def main():
    # Chemin du fichier log
    log_file_path = "C:/ELK/donnees/chatbot_log/chat.json"

    # Configurer le répertoire pour les logs
    setup_logging(log_file_path)

    # Initialiser le client Gradio
    client = Client("https://fb9c84fec32af92fa2.gradio.live/")

    print("Chatbot en ligne. Tapez 'exit' pour quitter.")

    while True:
        # Lire le message de l'utilisateur
        message = input("Vous: ")

        # Quitter la boucle si l'utilisateur tape 'fin'
        if message.lower() == 'fin':
            print("Fin de la session.")
            break

        # Envoyer le message au chatbot et obtenir la réponse
        try:
            result = client.predict(message=message, api_name="/predict")
            response = result.strip()  # Nettoyer la réponse

            # Afficher la réponse du chatbot
            print(f"Chatbot: {response}")

            # Créer une entrée JSON pour le message et la réponse
            log_entry = {
                "message": message,
                "response": response
            }

            # Enregistrer l'entrée JSON dans le fichier
            log_to_json(log_file_path, log_entry)

        except Exception as e:
            error_message = f"Erreur lors de l'envoi du message: {e}"
            print(error_message)

            # Enregistrer l'erreur dans le fichier JSON
            log_entry = {
                "error": error_message
            }
            log_to_json(log_file_path, log_entry)


if __name__ == "__main__":
    main()

#En dessous sont édités les instructions à mettre dans le fichier de configuration logstash
#Il suffit juste d'enlever le caractère '#' au début de chaque ligne
#Sur chaque ligne, enlevez le caractère '#' une seule fois

#input {
#  file {
#    path => "C:/ELK/donnees/chatbot_log/chat.json"  # Chemin vers votre fichier de logs JSON
#    start_position => "beginning"
#    sincedb_path => "C:/ELK/donnees/chatbot_log/base_lecture/sincedb"  # Assure que Logstash commence à lire depuis le début à chaque démarrage
#    codec => "json"  # Indique que les logs sont au format JSON
#  }
#}

#filter {
#  # Assurez-vous que les champs 'message' et 'response' existent
#  if [message] and [response] {
#    # Exemple de filtre pour extraire des informations supplémentaires (facultatif)
#    # grok {
#    #   match => { "message" => "%{GREEDYDATA:message}" }
# }
# } else {
#    # En cas de ligne de log incorrecte, marquer le message comme une erreur
#   mutate {
#     add_field => { "error_message" => "Ligne de log invalide: %{[message]}" }
#   }
#}
#}

#output {
#  elasticsearch {
#    hosts => ["http://localhost:9200"]  # Adresse de votre instance Elasticsearch
#    index => "index_chatbot"  # Index dans Elasticsearch
#    document_id => "%{[@metadata][_id]}"  # (Optionnel) Spécifiez un ID de document si vous avez un champ d'identifiant unique
#  }

#  # Vous pouvez également ajouter un output pour la sortie STDOUT pour débogage
#  stdout {
#    codec => rubydebug
#  }
#}


##Instructions à mettre dans le fichier chatbot.sh 
##Veuillez décomenter chaque ligne lors de l'édition du fichier chatbot.sh
#commande:"/usr/share/logstash/bin/logstash -f /chemin/vers/lefichier/chatbot.conf

#while true; do

#   $commande
#   sleep 600 #Attendre 10min, vous pouvez modifier le nombre de seconde

#done

