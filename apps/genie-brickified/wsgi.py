from geniebackend.endpoints import app

if __name__ == '__main__':

    certificate = '/etc/letsencrypt/live/bd-datas3.ucsd.edu/fullchain.pem'
    key = '/etc/letsencrypt/live/bd-datas3.ucsd.edu/privkey.pem'
    ssl_context = (certificate, key)
    app.run(host='0.0.0.0',
            port=5000,
            ssl_context=ssl_context,
            )
