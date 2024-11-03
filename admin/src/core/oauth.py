from authlib.integrations.flask_client import OAuth

class OAuthCedica:
    
    def __init__(self, app=None):
        self.oauth = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
        
        self.oauth = OAuth(app)
        
        self.oauth.register(
            name='google',
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        
        app.oauth = self.oauth
        
        return app
    
    @property
    def client(self):
        return self.oauth
    
    @client.setter
    def client(self, valor):
        self.oauth = valor
        
oauth = OAuthCedica()