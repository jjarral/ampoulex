from app import create_app

application = create_app()

if __name__ == '__main__':
    # Cloud Run sets the PORT environment variable automatically
    import os
    port = int(os.environ.get('PORT', 8080))
    application.run(host='0.0.0.0', port=port, debug=False)