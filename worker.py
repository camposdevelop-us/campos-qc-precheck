from src.main import app

def start():
    app.run(host='0.0.0.0', port=8080)
   
   
if __name__ == '__main__':
    start()