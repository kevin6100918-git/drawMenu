from response import response
import githubImageHandler
from htmlResponseModel import return_render_html


def lambda_handler(event: dict, context: dict):
    
    htmlContent = return_render_html(
        {
            "breakfast": githubImageHandler.get_menu_list("breakfast"),
            "dinner": githubImageHandler.get_menu_list("dinner")
        }
    )

    return response("text/html", 200, htmlContent)
