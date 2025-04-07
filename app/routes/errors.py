from flask import render_template, current_app

def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', 
                               error_title="Page Not Found",
                               error_message="The page you are looking for does not exist."), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html',
                               error_title="Server Error",
                               error_message="An unexpected error occurred. Please try again later."), 500
    
    @app.errorhandler(413)
    def too_large_error(error):
        return render_template('error.html',
                               error_title="File Too Large",
                               error_message=f"The file you uploaded is too large. Maximum allowed size is {app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024):.1f} MB."), 413