headContext = '''
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>菜單管理</title>
    <style>
        /* 主要的網頁樣式 */
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #4a2c2a;
            background-color: #fff9f5;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        h1 {
            font-size: 2em;
            margin-bottom: 20px;
            color: #8b5a4b;
            text-align: center;
        }
        #menuCategory {
            font-size: 18px;
            padding: 10px 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            border: 1px solid #d9b7a3;
            background-color: #ffe8d6;
            color: #5a3e3b;
            cursor: pointer;
        }
        button {
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            background-color: #d99873;
            color: #fff;
            cursor: pointer;
            margin-bottom: 20px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #c6855a;
        }

        .restaurant {
            position: relative;
            border-radius: 10px;
            width: 200px; /* 固定寬度 */
            height: 250px; /* 固定高度 */
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            transition: transform 0.3s, box-shadow 0.3s;
            background-color: #fdf3e8;
            color: #4a2c2a;
            display: flex;
            flex-direction: column;
            justify-content: flex-end; /* 將內容放在底部 */
        }

        .restaurant img {
            width: 100%;
            height: 100%;
            object-fit: cover; /* 自動填充圖片，符合高度或寬度 */
            object-position: center; /* 圖片居中顯示 */
            border-radius: 10px 10px 0 0;
        }

        .restaurant-name {
            position: absolute;
            bottom: 0;
            width: 100%;
            padding: 10px;
            font-size: 1em;
            font-weight: bold;
            color: #fff;
            text-align: center;
            background-color: rgba(0, 0, 0, 0.5); /* 半透明背景 */
            border-radius: 0 0 10px 10px; /* 底部圓角 */
            z-index: 1;
        }

        .menu-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            max-width: 100%;
        }

        /* 上傳彈窗樣式 */
        #uploadModal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .modal-content {
            background-color: #ffe8d6;
            padding: 20px;
            width: 300px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
            color: #5a3e3b;
        }
        .modal-content input,
        .modal-content select,
        .modal-content button {
            margin: 10px 0;
            padding: 10px;
            width: 100%;
            font-size: 16px;
        }
        .modal-content input,
        .modal-content select {
            width: 75%;
        }
        .modal-content button {
            background-color: #d99873;
            color: white;
            border: none;
            cursor: pointer;
        }
        .modal-content button:hover {
            background-color: #c6855a;
        }
        .close-btn {
            background-color: #c74b35;
            color: white;
            padding: 5px 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            float: right;
        }

        /* 上傳中動畫的樣式 */
        #uploadingModal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            align-items: center;
            justify-content: center;
            z-index: 1001;
        }
        
        .uploading-content {
            background-color: #fff;
            padding: 20px;
            width: 200px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }

        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 10px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* 刪除功能選單樣式 */
        .menu-icon {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            background-color: rgba(255, 235, 230, 0.8);
            border-radius: 50%;
            padding: 5px;
            transition: background-color 0.3s;
        }
        .menu-icon:hover {
            background-color: #ff7961;
        }
        .delete-option {
            display: none;
            position: absolute;
            top: 40px;
            right: 10px;
            background-color: #fff;
            border: 1px solid #d99873;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            color: #8b5a4b;
            z-index: 10;
        }
        .delete-option:hover {
            background-color: #ffe8d6;
            color: #c74b35;
        }

        /* 手機顯示樣式 */
        @media (max-width: 768px) {
            .restaurant {
                width: 45%; /* 調整寬度以便手機顯示兩張菜單 */
                height: auto; /* 高度自適應 */
            }
        }
    </style>
'''

basicBody = '''
    <h1>餐廳菜單管理系統</h1>
    <select id="menuCategory" onchange="redirectBasedOnSelection()">
        <option value="breakfast">早餐</option>
        <option value="dinner">晚餐</option>
    </select>
    <button onclick="openModal()">上傳新菜單</button>

    <div class="menu-container" id="menuContainer">
        <!-- 餐廳菜單圖片將顯示在這裡 -->
    </div>

    <!-- 上傳彈窗 -->
    <div id="uploadModal">
        <div class="modal-content">
            <button class="close-btn" onclick="closeModal()">×</button>
            <h2>上傳新菜單</h2>
            <input type="text" id="menuName" placeholder="菜單名稱">
            <input type="file" id="menuFile">
            <select id="menuType">
                <option value="breakfast">早餐</option>
                <option value="dinner">晚餐</option>
            </select>
            <button onclick="uploadMenu()">提交</button>
        </div>
    </div>

    <!-- 上傳中彈窗 -->
    <div id="uploadingModal">
        <div class="uploading-content">
            <div class="loader"></div>
            上傳中...
        </div>
    </div>
'''

basicScript = '''
    <script>
        function redirectBasedOnSelection() {
            const category = document.getElementById('menuCategory').value;
            if (category) {
                loadMenuImages();
            }
        }

        function openModal() {
            document.getElementById('uploadModal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('uploadModal').style.display = 'none';
        }

        function showUploadingModal() {
            document.getElementById('uploadingModal').style.display = 'flex';
        }

        function hideUploadingModal() {
            document.getElementById('uploadingModal').style.display = 'none';
        }

        function uploadMenu() {
            const menuName = document.getElementById('menuName').value;
            const menuFile = document.getElementById('menuFile').files[0];
            const menuType = document.getElementById('menuType').value;

            if (!menuName || !menuFile || !menuType) {
                alert('請填寫所有欄位');
                return;
            }

            if (!menuFile.type.startsWith('image/')) {
                console.log("不是圖片格式");
                return;
            }

            showUploadingModal(); // 顯示上傳中彈窗

            const reader = new FileReader();
            reader.readAsArrayBuffer(menuFile);
            reader.onload = function(event) {
                // 壓縮圖片
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const img = new Image();
                let blob = new Blob([event.target.result]);
                let blobURL = URL.createObjectURL(blob);
                img.src = blobURL;
                img.onload = function() {
                    const MAX_WIDTH = 1080;
                    const MAX_HEIGHT = 2400;
                    let width = img.width;
                    let height = img.height;

                    if (width > height) {
                        if (width > MAX_WIDTH) {
                            height *= MAX_WIDTH / width;
                            width = MAX_WIDTH;
                        }
                    } else {
                        if (height > MAX_HEIGHT) {
                            width *= MAX_HEIGHT / height;
                            height = MAX_HEIGHT;
                        }
                    }

                    canvas.width = width;
                    canvas.height = height;
                    ctx.drawImage(img, 0, 0, width, height);
                    const fileData = canvas.toDataURL(menuFile.type)  // 取得 base64 編碼的圖片數據

                    const webUrl = window.location.href + '/upload';

                    fetch(webUrl, {
                        method: 'POST',
                        body: JSON.stringify({
                            category: menuType,
                            name: menuName,
                            fileName: menuFile.name,
                            fileData: fileData
                        })
                    })
                    .then(response => {
                        if (!response.ok) {
                            // 自行根據 HTTP 狀態碼處理錯誤
                            if (response.status === 413) {
                                alert('圖片太大，請嘗試壓縮後再上傳');
                            } else {
                                alert(`上傳失敗，伺服器回傳錯誤碼 ${response.status}`);
                            }
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        alert('上傳成功');
                        closeModal();
                        location.reload();
                    })
                    .catch(error => {
                        console.error('上傳失敗:', error);
                        alert('上傳失敗，請重試');
                    });
                };
            }
        }

        function deleteMenu(menuType, menuName) {
            const confirmDelete = confirm(`確定要刪除 ${menuName} 嗎？`);
            if (!confirmDelete) return;

            const webUrl = window.location.href + '/delete';

            fetch(webUrl, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ category: menuType, name: menuName })
            })
            .then(response => response.json())
            .then(data => {
                alert(`${menuName} 已成功刪除`);
                location.reload();
            })
            .catch(error => {
                console.error('刪除失敗:', error);
                alert('刪除失敗，請重試');
            });
        }

        function loadMenuImages() {
            const category = document.getElementById('menuCategory').value;
            const menuContainer = document.getElementById('menuContainer');
            menuContainer.innerHTML = "";

            const restaurantData = {
                REPLACE_THE_RESTAURANT_DATA
            };

            if (restaurantData[category]) {
                restaurantData[category].forEach(restaurant => {
                    const restaurantDiv = document.createElement('div');
                    restaurantDiv.className = 'restaurant';

                    const img = document.createElement('img');
                    img.src = restaurant.image;
                    img.alt = restaurant.name;

                    const name = document.createElement('a');
                    name.className = 'restaurant-name';
                    name.textContent = restaurant.name;
                    name.href = restaurant.image;

                    // 刪除圖示和選項
                    const iconDiv = document.createElement('div');
                    iconDiv.className = 'menu-icon';
                    iconDiv.innerHTML = '⋮';
                    iconDiv.onclick = () => {
                        deleteOption.style.display = deleteOption.style.display === 'block' ? 'none' : 'block';
                        console.log(deleteOption.style.display)
                    };

                    const deleteOption = document.createElement('div');
                    deleteOption.className = 'delete-option';
                    deleteOption.textContent = '刪除';
                    deleteOption.onclick = () => {
                        deleteMenu(category, restaurant.name);
                    };

                    restaurantDiv.appendChild(img);
                    restaurantDiv.appendChild(iconDiv);
                    restaurantDiv.appendChild(deleteOption);
                    restaurantDiv.appendChild(name);
                    menuContainer.appendChild(restaurantDiv);
                });
            }
        }

        window.onload = loadMenuImages;
    </script>
'''

def fill_restaurant(imgList):
    replaceData = f"breakfast:[\n"
    for content in imgList["breakfast"]:
        replaceData += f"\t\t\t{{ name: '{content[0]}', image: '{content[1]}' }},\n"
    replaceData += "\t\t],\n"

    replaceData += f"\t\tdinner:[\n"
    for content in imgList["dinner"]:
        replaceData += f"\t\t\t{{ name: '{content[0]}', image: '{content[1]}' }},\n"
    replaceData += "\t\t]"

    filledScript = basicScript.replace(
        "REPLACE_THE_RESTAURANT_DATA",
        replaceData
    )
    return filledScript
# print(fill_restaurant("breakfast", [["1", "2"], ["3", "4"]]))

def return_render_html(imgList):
    return f'''
        <!DOCTYPE html>
        <html lang="zh">
        <head>
            {headContext}
        </head>
        <body>
            {basicBody}
            {fill_restaurant(imgList)}
        </body>
        </html>
    '''