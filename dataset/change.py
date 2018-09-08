import os
from PIL import Image

yourpath = os.getcwd()
for root, dirs, files in os.walk(yourpath, topdown=False):
    count = 0
    for name in files:
        if os.path.splitext(os.path.join(root, name))[1].lower() == ".tiff":
            count = count + 1
            outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
            im = Image.open(os.path.join(root, name))
            im.mode = 'I'
            # print "Generating jpeg for %s" % name
            im.thumbnail(im.size)
            im.save(outfile, "JPEG", quality=100)
            # filename = "count" + str(count) + '.jpeg'
            # im.point(lambda i:i*(1./256)).convert('L').save('my.jpeg')
