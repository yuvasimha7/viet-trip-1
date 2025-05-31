from app import create_app

app = create_app()  # <-- Call the function, don't just import it

if __name__ == '__main__':
    with app.app_context():  # Now this will work
        app.run(debug=True)
