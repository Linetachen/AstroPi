from PIL import Image

def modify_colour(image_path):
  img = Image.open(image_path)
  width, height = img.size
  for x in range(width):
    for y in range(height):
      r, _, _ = img.getpixel((x,y))
      img.putpixel((x,y)(r, 0, 0))
      output_path = Image.path.replace('jpg', 'changed.jpg')
      (img.save(output_path))
      print('modified and saved')

modify_colour('leaves.jpg')