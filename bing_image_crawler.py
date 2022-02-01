import math,aiohttp,asyncio,re,os
from aiomultiprocess import Pool
# from itertools import zip_longest
from multiprocessing import Value   # 共享記憶體
from aiofile import async_open
from pathlib import Path

def get_request_urls(query=None,img_num=0)->list:
    """
    get urls for requesting according to the query and numbers of image that wants to download
    :param query: keyword of image
    :param img_num: numbers of image
    :return: requesting urls
    """
    request_urls_num=math.ceil(img_num/35)
    urls=[f"https://www.bing.com/images/async?q={query}&first={1+35*i}&count=35&cw=1177&ch=577&tsc=ImageBasicHover&datsrc=I&mmasync=1&SFX={i+1}" for i in range(request_urls_num)]
    return urls

# async def get_html(session,url):
async def get_html(url):
    # async with session.get(url,ssl=False) as resp:   # ssl=False跳過ssl憑證驗證
    async with aiohttp.request("GET",url) as resp:
        assert resp.status==200
        return await resp.text()

async def download_image(img_url,storing_path,query,current_num_of_img,img_num):
    suffix=img_url[img_url.rfind('.'):]
    illegal_suffixes=(".com",".tw",".cn","io")
    for illegal_suffix in illegal_suffixes:
        if illegal_suffix in suffix or len(suffix)>9:   # 有些圖片網址會沒有圖片副檔名而導致副檔名錯誤，手動修正副檔名
            suffix=".jpg"
    folder_path=Path(storing_path+os.sep+query)
    if not folder_path.exists():
        os.mkdir(folder_path)
    with current_num_of_img.get_lock():
        if current_num_of_img.value<img_num:
            try:
                async with aiohttp.request("GET",img_url) as resp:
                    assert resp.status==200
                    # Path物件可以透過除法運算(/)來進行路徑的合併
                    async with async_open(folder_path/(str(current_num_of_img.value+1)+suffix),"wb") as afd:
                        async for line in resp.content:   # 預設以行來疊代
                            await afd.write(line)
                        current_num_of_img.value+=1
            except AssertionError as e:
                print(f"{e}\n{resp.url}",flush=True)
            except FileNotFoundError as e:
                print(f"{e}\n{img_url}",flush=True)
            except aiohttp.ClientConnectorError as e:
                print(f"{e}\n{resp.url}",flush=True)
            except aiohttp.ClientPayloadError as e:
                print(f"{e}\n{resp.url}",flush=True)

async def main(urls,query,img_num,storing_path=os.getcwd()):
    # async with aiohttp.ClientSession() as session:   # multiprocess pool在map()或starmap()時會用pickle序列化和反序列化傳遞給func的參數，但ClientSession物件無法序列化，所以改用aiohttp.request()
        async with Pool() as pool:
            """
            starmap(func,iterable)的iterable是一個可疊代序列，裡面又有好幾個可疊代小序列，他會分派process去將每個小序列一一作為func的參數來執行
            zip(*iterables,strict=False)會將多個iterable中的元素一一對應組合成一個zip object，當iterable的長度都不同時會以最短的為主，其他多的元素會直接被捨棄，如果strict被設成True，會強制要求所有iterables長度都要相同否則會引發ValueError，zip(*)為解壓縮
            itertools.zip_longest(*iterables,fillvalue=None)如果iterables長度不同，會用fillvalue填補較短的iterable直到最長的iterable中的元素都被zip到
            itertools.repeat(object[,times])times參數用來指定要重複object的次數，如果沒有指定times參數就會重複無限次object
            """
            # async for html in pool.starmap(get_html,zip_longest((session,),urls,fillvalue=session)):   # 等價zip(repeat(session),urls)
            pattern=re.compile(r"murl&quot;:&quot;(.*?)&quot;,&quot;tu")
            current_num_of_img=Value("i",0)   # 創建一個ctypes整數型態的共享記憶體變數，初始值為0
            async for html in pool.map(get_html,urls):
                img_urls_list=pattern.findall(html)
                for img_url in img_urls_list:
                    img_url=img_url.rsplit('?',1)[0]   # 有些圖片網址副檔名後面還會有其他網址參數，是以'?'為開頭接在副檔名後面，此行用來消除'?'之後的網址參數
                    await download_image(img_url,storing_path,query,current_num_of_img,img_num)

if __name__=="__main__":
    urls=get_request_urls(query:=input("請輸入圖片關鍵字:"),img_num:=int(input("請輸入要下載的數量:")))
    if storing_path:=input("請輸入要儲存的路徑，預設為當前工作目錄:"):
        asyncio.run(main(urls,query,img_num,storing_path))
    else:
        asyncio.run(main(urls,query,img_num))