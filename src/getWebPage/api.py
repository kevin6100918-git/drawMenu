from response import response

import getImageHandler
from htmlResponseModel import return_render_html


def lambda_handler(event: dict, context: dict):
    
    htmlContent = return_render_html(
        {
            "breakfast": getImageHandler.get_menu_list("breakfast"),
            "dinner": getImageHandler.get_menu_list("dinner")
        }
    )

    return response("text/html", 200, htmlContent)
