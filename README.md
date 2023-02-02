[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://github.com/jacky0115/bing_image_crawler#readme) [![awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/jacky0115/bing_image_crawler.git) [![Download link](https://img.shields.io/badge/Download%20now-Link-green?style=social&logo=appveyor)](https://github.com/jacky0115/bing_image_crawler/archive/refs/heads/main.zip)
# bing_image_crawler 🕷️
A crawler for Bing image.


## How to use it?
1. `git clone https://github.com/jacky0115/bing_image_crawler.git` or click `Code` button, then click `Download ZIP`.
2. Open the folder you just downloaded, you have to unzip the zipped folder first if you use the `Download ZIP` method.
3. If you have Python in your computer, then open the terminal and `cd` to the folder where you just downloaded. For example, if you download bing_image_crawler to C:\Users\username\Downloads on Windows, then type `cd C:\Users\username\Downloads\bing_image_crawler` in the terminal. Similarly, do the same procedure on Linux or mac OS.
4. Type `pip install -r requirements.txt` in the terminal to install all python modules that bing_image_crawler would need.
5. Type `python bing_image_crawler.py` on Windows, `python3 bing_image_crawler.py` on Linux and mac OS to activate bing_image_crawler.
6. It will first ask you what kinds of picture you want to download, just enter the query and then press Enter.
7. Then it will ask you the numbers of image that you want to download, just enter the number and then press Enter.
8. Finally, it will ask you about download folder location. bing_image_crawler will create a folder which is named after you query.
9. Go make some coffee☕ and after you finish your low tea, you will see all images in the folder.

📝P.S. : If you see some urls in the terminal. That means bing_image_crawler can't download those pictures for some reason. You can download them manually if necessary.

## Future change
- [ ] Use [aiopipe](https://github.com/kchmck/aiopipe) instead of multiprocessing.Value to communicate between processes in pool. Then I can use pool.starmap() to invoke download_image which is an async function. And that would definitely make bing_image_crawler faster. But actually, I'm not sure that objects return from aiopipe can be pickled by pool.starmap(). I will try it someday.
