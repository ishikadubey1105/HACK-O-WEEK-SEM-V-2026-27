from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Starting Library Management System API...")
    print("Visit http://127.0.0.1:5000/ to see all endpoints")
    app.run(debug=True, port=5000)
