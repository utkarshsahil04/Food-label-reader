import cv2
from pyzbar.pyzbar import decode
import requests

HARMFUL_LIST=[
"sodium nitrite","nitrate","butylated hydroxyanisole","butylated hydroxytoluene","potassium bromate","propyl gallate","red 3"," Red 40","yellow 5","yellow 6","blue 1","blue 2","aspartame","saccharin","sucralose","acesulfame potassium","cyclamate","monosodium glutamate","disodium inosinate","partially hydrogenated oils","polysorbate 80","carrageenan","carboxymethylcellulose","Artificial Flavor","diacetyl","vegetable oil","maltodextrin","sorbitol","mannnitol","erythritol","bleached flour","modiefied flour","modiedied corn starch","sodium benzoate","sodium phosphate","propylene glycol","calcium propionate","E502(ii)","E500(ii)","Iodised Salt","sugar","sucre"

]
def image_qr_code(image_path):
    image=cv2.imread(image_path)
    # detector=cv2.QRCodeDetector()
    # data,bbox,_=detector.detectAndDecode(image)
    detected_barcodes = decode(image)
    # for obj in detected_barcodes:
    #     print("Detected Barcode:", obj)
    #     print("Type:", obj.type)

    for obj in detected_barcodes:
        print("QR/BAR code data:",obj.type,"code:" ,obj.data.decode('utf-8'))
        if obj.type in ['QRCODE', 'EAN13','ENA8','UPC']:
            return obj.data.decode('utf-8')
    else:
        print("No QR code Detected or decoding failed")
        return None

def fetch_ingredients_from_url(barcode):
    url=f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response=requests.get(url)
        response.raise_for_status()
        data=response.json()

        
        if data.get("status")==1:
            ingredients_text=data["product"].get("ingredients_text","")
            return ingredients_text
        else:
            print("Product not found in Open Food Facts.")
            return ""
    except requests.RequestException as e:
        print (f"Network error:{e}")
        return ""
    
def detect_harmful_ingredients(ingridients):
    harmful_found=[]
    ingridients=[ingridients.lower() for ingridients in ingridients]

    for ingridients in ingridients:
        if any(harmful in ingridients for harmful in HARMFUL_LIST):
            harmful_found.append(ingridients)
        
    return harmful_found

def main(image_path):
    qr_data=image_qr_code(image_path)
    if qr_data is None:
        return
    ingredients_list=[]
    ingredients=fetch_ingredients_from_url(qr_data)
    # if qr_data.startswith("http"):
    if ingredients:
        ingredients_list=[ing.strip() for ing in ingredients.split(",")]
    else:
        print("No ingridients found in product data :")
        return
        
    harmful_ingridients=detect_harmful_ingredients(ingredients_list)
    
        # ingredients_list=[qr_data]
                     
    # if not ingredients_list:
    #     print("No ingredients data found")
    #     return

    if harmful_ingridients:
        print("Harmful Ingridients found")
        for item in harmful_ingridients:
            print(f" ,{item}")
    else:
        print("No Harmful ingredients detected")
if __name__=="__main__":
    main("nut3.png")


    # yaha pe bahoot hi gande tarike se type ho raha ha 
    # 