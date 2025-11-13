from main import app

if __name__ == "__main__":
    print("wsgi starting..")
    app.run(debug=True,host='0.0.0.0',port=7000)