from os import environ

class response_html():
    def return_singal_image(imgFileName, encoded_image):
        return f'''
            <html style="height: 100%;">
            <head>
                <meta name="viewport" content="width=device-width, minimum-scale=0.1">
                <title>{imgFileName}</title>
            </head>
            <body style="margin: 0px; height: 100%; background-color: rgb(14, 14, 14);"><img
                    style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;"
                    src="data:image/jpeg;base64,{encoded_image}"></body>
            </html>
        '''
    
    def return_menu_list(resource, imgList):
        # print(f"imgList: {imgList}")
        baseHtml = '''
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }

                    td {
                        width: 33.33%;
                    }

                    img {
                        max-width: 100%;
                        height: auto;
                        display: block;
                        margin: 0 auto;
                    }
                </style>
                <title>菜單總攬</title>
            </head>
            <body style="width: 94%; align-content: center;">
                <form id="imageForm" action="#" method="post">
                    <table border="1">
        '''
        for index, content in enumerate(imgList):
            imgFileName, encoded_image = content
            if (index+1) % 3 == 1:
                baseHtml += f'''
                        <tr>
                            <td>
                                <img src="data:image/jpeg;base64,{encoded_image}" alt="{imgFileName}" onclick="sendRequest(event)">
                            </td>
                '''
            elif (index+1) % 3 == 2:
                baseHtml += f'''
                            <td>
                                <img src="data:image/jpeg;base64,{encoded_image}" alt="{imgFileName}" onclick="sendRequest(event)">
                            </td>
                '''
            else:
                baseHtml += f'''
                            <td>
                                <img src="data:image/jpeg;base64,{encoded_image}" alt="{imgFileName}" onclick="sendRequest(event)">
                            </td>
                        </tr>
                '''
        if resource  == "/draw/menu":
            baseHtml += '''
                        </table>
                    </form>

                    <script>
                        function sendRequest(event) {
                            const imgFileName = event.target.alt;
                            // Construct the URL for the GET request
                            let apiUrl = window.location.href; // Replace with your actual API endpoint
                            apiUrl = apiUrl.replace(/\/menu$/, '');
                            apiUrl += '?img=';
                            apiUrl += imgFileName;
                            console.log(apiUrl)

                            // Send the GET request using the Fetch API
                            fetch(apiUrl, {
                                method: 'GET',
                                // headers: {
                                    // 'Content-Type': 'application/json',
                                    // Add any additional headers if needed
                                // },
                                // You can include a request body if required
                                // body: JSON.stringify({ img: `${imgFileName}` }),
                            })
                            .then(response => {
                                if (response.ok) {
                                    window.location.href = apiUrl;
                                } else {
                                    alert('Failed to send GET request for image: ' + imgFileName);
                                }
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                alert('Error sending GET request for image: ' + imgFileName);
                            });
                        }
                    </script>
                </body>
                </html>
            '''
        elif resource == "/draw/menu/delete":
            baseHtml += '''
                        </table>
                    </form>

                    <script>
                        function sendRequest(event) {
                            const imgFileName = event.target.alt;
                            // Construct the URL for the DELETE request
                            let apiUrl = window.location.href; // Replace with your actual API endpoint
                            apiUrl = apiUrl.replace(/\/menu\/delete$/, '');
                            console.log(apiUrl)

                            // Send the DELETE request using the Fetch API
                            fetch(apiUrl, {
                                method: 'DELETE',
                                headers: {
                                    'Content-Type': 'application/json',
                                    // Add any additional headers if needed
                                },
                                // You can include a request body if required
                                body: JSON.stringify({ 'img': imgFileName}),
                            })
                            .then(response => {
                                if (response.ok) {
                                    alert('DELETE request sent for image: ' + imgFileName);
                                    window.location.href = apiUrl + `/menu`;
                                } else {
                                    alert('Failed to send DELETE request for image: ' + imgFileName);
                                }
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                alert('Error sending DELETE request for image: ' + imgFileName);
                            });
                        }
                    </script>
                </body>
                </html>
            '''
        return baseHtml