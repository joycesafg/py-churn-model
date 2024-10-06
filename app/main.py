from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
import joblib
import pandas as pd
import os
from datetime import datetime


# Carregar variáveis de ambiente
load_dotenv()


templates = Jinja2Templates(directory="templates")


# Conectar ao MongoDB
def connect(collection_name):
    """
    Establishes a connection to a MongoDB database and returns a collection object.
    This function retrieves MongoDB credentials from environment variables, constructs
    a connection string, and connects to a MongoDB cluster. It then pings the database
    to ensure the connection is successful and returns a specific collection from the
    database.
    Returns:
        pymongo.collection.Collection: The collection object for 'credit_risk_features_input'
        from the 'ML_db' database.
    Raises:
        Exception: If the connection to the MongoDB cluster fails.
    """
    MONGODB_USER = os.getenv("MONGO_USER")
    MONGODB_PASSWORD = os.getenv("MONGO_PASS")

    login = f"{MONGODB_USER}:{MONGODB_PASSWORD}"
    cluster = "clusterdatamaster.sehlms5.mongodb.net"
    app_name = "retryWrites=true&w=majority&appName=ClusterDataMaster"

    client = MongoClient(f"mongodb+srv://{login}@{cluster}/?{app_name}")

    # Conexão com o banco de dados
    db = client.get_database("ML_db")
    model_collection = db.get_collection(collection_name)

    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return model_collection


def save_to_mongo(data, collection_name):
    collection = connect(collection_name)
    collection.insert_one(data)


# Carregar o modelo
def load_model(pkl_path):
    return joblib.load(pkl_path)


# Caminho do modelo
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

# Carregar o modelo uma vez no início
model = load_model(model_path)


# Função para obter a previsão do modelo
def get_model(df):
    prediction = model.predict_proba(df)
    print(prediction[:, 1])
    return 1 if prediction[:, 1] >= 0.1 else 0


# Inicia o FastAPI
app = FastAPI()


# Define a estrutura dos dados de entrada
class InputData(BaseModel):
    id: int


# Define a estrutura dos dados de saída
class PredictionOutput(BaseModel):
    id: str
    prediction: str


# Cria a conexão com o banco de dados
model_collection = connect("credit_risk_features_input")


# Rota para obter o predction
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("front.html", {"request": request})


@app.post("/predict")
async def predict(
    request: Request,
    background_tasks: BackgroundTasks,
    id: int = Form(...),
):

    document = model_collection.find_one({"_id": id})

    if not document:
        prediction = "Document not found"
    else:
        document.pop("_id", None)
        print(document)
        df = pd.DataFrame([document])

        prediction = get_model(df)

    json_return = {
        "_id": str(id),
        "aplica_promo": str(prediction),
        "processing_time": datetime.now().isoformat(),
    }
    background_tasks.add_task(save_to_mongo, json_return, "output_churn_model")

    return templates.TemplateResponse(
        "front.html", {"request": request, "result": json_return}
    )
