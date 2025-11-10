from main import app

if __name__ == "__main__":
    # app.register_blueprint(app.main,url_prefix='/')
    # # # url_prefix указывает URL в контексте которого будет доступна часть данного Blueprint
    # app.register_blueprint(app.sitepart,url_prefix='/sitepart')
    print("wsgi starting..")
    #app.run()