from config import drone_api

if __name__ == '__main__':
    drone_api.run(host='0.0.0.0', port=5000, debug=True)
