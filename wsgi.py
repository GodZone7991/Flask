from application import create_app


if __name__ == "__main__":
    create_app().run(threaded=True)
else:
    app = create_app()