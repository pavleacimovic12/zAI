from app_efficient import app

# Expose app for Posit Connect
application = app

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)