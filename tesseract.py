import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def boxes(img):
    h, w = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (111, 111, 111), 1)

    return img


def show_res(image, text):
    print("  :  ", text, "\n___________\n")
    cv2.imshow("image", image)
    cv2.waitKey()


def get_text_from_image(image):
    try:
        image = cv2.GaussianBlur(image, (3,3), 0)
        tess_res = pytesseract.image_to_string(image, lang='eng', config='--oem 1 --psm 6')
        res = tess_res.replace('\n\x0c','')
        print(res)
        return res
        # boxes_img = boxes(image)  # BOXES
        # show_res(boxes_img, res)
    except Exception:
        print('Это что ещё такое?')
