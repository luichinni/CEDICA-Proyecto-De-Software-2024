from minio import Minio

class Storage():
    
    def __init__(self, app=None):
        self._client = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        minio_server = app.config["MINIO_SERVER"]
        access_key = app.config["MINIO_ACCESS_KEY"]
        secret_key = app.config["MINIO_SECRET"]
        secure = app.config["MINIO_SECURE"]
        
        self._client = Minio(
            minio_server, access_key=access_key, secret_key=secret_key, secure=secure
        )
        
        app.storage = self._client
        
        return app
    
    @property
    def client(self):
        return self._client
    
    @client.setter
    def client(self, valor):
        self._client = valor
        
storage = Storage()