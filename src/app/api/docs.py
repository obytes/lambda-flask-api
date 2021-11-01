from app.api.conf.settings import AWS_API_GW_MAPPING_KEY


def get_swagger_ui():
    title = "Lambda Flask API Starter"
    swagger_js_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"
    swagger_css_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css"
    swagger_favicon_url = "https://fastapi.tiangolo.com/img/favicon.png"
    swagger_specification_url = f"/{AWS_API_GW_MAPPING_KEY}/v1/swagger.json"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        url: '{swagger_specification_url}',
    """

    html += """
            dom_id: '#swagger-ui',
            presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            layout: "BaseLayout",
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true
        })"""

    html += """
        </script>
        </body>
        </html>
        """
    return html
