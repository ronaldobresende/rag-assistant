import weaviate
import sys
from utils.file_utils import load_file

WEAVIATE_URL = "http://localhost:8080/"

# Configura o cliente Weaviate
client = weaviate.Client(
    url=WEAVIATE_URL,
)

class_name = "Document"

# Testa a conexão com o Weaviate
try:
    client.is_ready()
    print("Conexão com o Weaviate está OK.")
except Exception as e:
    print(f"Erro ao conectar com o Weaviate: {e}")
    sys.exit(1)

def obtem_id_do_objeto():
    query = """
    {
        Get {
            Document(where: {
                path: ["title"],
                operator: Equal,
                valueString: "garantias"
            }) {
                _additional {
                    id
                }
            }
        }
    }
    """
    response = client.query.raw(query)
    documents = response['data']['Get']['Document']
    if not documents:
        return None
    return documents[0]['_additional']['id']    

# Verifica se a classe já existe
existing_classes = client.schema.get()['classes']
class_names = [cls['class'] for cls in existing_classes]

if class_name in class_names:
    # Apaga a classe existente
    client.schema.delete_class(class_name)
    print(f"Class {class_name} deleted.")

# Define a nova classe
weaviate_class = {
    "class": class_name,
    "description": "A class to store documents",
    "properties": [
        {
            "name": "title",
            "dataType": ["string"]
        },
        {
            "name": "content",
            "dataType": ["text"]
        }
    ]
}

# Cria a nova classe
client.schema.create_class(weaviate_class)

# Adiciona um documento de exemplo ao Weaviate
contexto = load_file("data/ingestors/garantias_v2.txt")
data_object = {
    "title": "garantias",
    "content": contexto,
}

# Atualiza o documento se ele já existir, caso contrário, cria um novo
objeto_id = obtem_id_do_objeto()
if objeto_id:
    client.data_object.update(data_object, class_name="Document", uuid=objeto_id)
else:
    client.data_object.create(data_object, "Document")

# Função para obter o contexto do Weaviate
def get_context():
    query = """
    {
        Get {
            Document(where: {
                path: ["title"],
                operator: Equal,
                valueString: "garantias"
            }) {
                content
            }
        }
    }
    """
    response = client.query.raw(query)
    return response['data']['Get']['Document'][0]['content']











