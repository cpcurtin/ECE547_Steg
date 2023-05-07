#import aspose.words as aw

#doc = aw.Document("Input.txt")

#extractedPage = doc.extract_pages(0, 1)
#extractedPage.save("Output.jpg")


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

font = ImageFont.truetype("arial.ttf", 50)
img = Image.new('RGB', (230, 230))
d = ImageDraw.Draw(img)
d.text((50, 50), 'Hello', fill=(255, 255, 255), font=font)
s = io.BytesIO()
img.save(r'C:\Users\John Pashapour\PythonProjects\Watermarking\Watermark-JPEG-with-8x8DCT-master\img.jpg')

