from flask import send_from_directory
import os

@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 errors"""
    try:
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    except:
        # Return empty response if favicon not found
        return '', 204
