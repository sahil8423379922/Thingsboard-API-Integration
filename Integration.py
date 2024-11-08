from flask import Flask, render_template, jsonify
from flask_cors import CORS
import logging
# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_pe import *
from tb_rest_client.rest import ApiException

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ThingsBoard REST API URL
url = "http://140.238.162.179:8080"

# Default Tenant Administrator credentials
username = "tenant@thingsboard.org"
password = "tenant"

@app.route('/api/data', methods=['GET'])
def get_data():
    # Same implementation as before
    with RestClientPE(base_url=url) as rest_client:
        try:
            rest_client.login(username=username, password=password)
            logging.info('Login Successful')

            page_size = 10
            page = 0
            devices = []

            while True:
                device_page = rest_client.get_tenant_devices(page_size=page_size, page=page)
                devices.extend(device_page.data)
                if device_page.has_next:
                    page += 1
                else:
                    break

            logging.info("Devices: \n%r", devices)
            return jsonify(devices)

        except ApiException as e:
            logging.exception(e)

@app.route('/devices', methods=['GET'])
def show_devices():
    with RestClientPE(base_url=url) as rest_client:
        try:
            rest_client.login(username=username, password=password)
            logging.info('Login Successful')

            page_size = 10
            page = 0
            devices = []

            while True:
                device_page = rest_client.get_tenant_devices(page_size=page_size, page=page)
                devices.extend(device_page.data)
                if device_page.has_next:
                    page += 1
                else:
                    break

            logging.info("Devices: \n%r", devices)

            # Render the template with devices data
            return render_template('devices.html', devices=devices)

        except ApiException as e:
            logging.exception(e)
            return "An error occurred while fetching devices."

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
