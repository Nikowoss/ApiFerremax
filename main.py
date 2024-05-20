from flask import Flask
from flask_cors import CORS

from routes import ProductoRoutes
from routes import ClienteRoutes
from routes import VendedorRoutes

from PayPal import paypal
from BancoNCH import Bnchapi

from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "nose"  
jwt = JWTManager(app)

@app.route('/')
def index():
  return 'API Ferremax'

#Blueprint
app.register_blueprint(paypal.main, url_prefix="/paypal")
app.register_blueprint(Bnchapi.main, url_prefix="/Bnchapi")
app.register_blueprint(ProductoRoutes.main, url_prefix="/Productos")
app.register_blueprint(ClienteRoutes.main, url_prefix="/Clientes")
app.register_blueprint(VendedorRoutes.main, url_prefix="/Vendedors")
app.run(host='0.0.0.0', port=81)
