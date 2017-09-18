import cv2.cv as cv

saveImagePath = 'D:/'
colorRed = [0, 0, 255]
colorGreen = [0, 255, 0]
colorBlue = [255, 0, 0]
colorWhite = [255, 255, 255]
colorBlack = [0, 0, 0]
colorAqua = [255, 255, 0]
colorFuchsia = [255, 0, 255]
colorYellow = [0, 255, 255]
stardardColors = [colorBlue, colorGreen, colorAqua, colorRed, colorFuchsia, colorYellow, colorWhite]


def createImg(depth=3):
    return cv.CreateImage((800, 480), 8, depth)


def saveImageFile(typeName, img):
    filename = saveImagePath + typeName + '.png'
    cv.SaveImage(filename, img)
    print typeName + '.png', '\t\t...\tok'


def createOneColorImage(color):
    img = createImg()
    cv.Set(img, color)
    return img


def create64GrayImage():
    img = createImg(1)
    cv.SetZero(img)
    for xPos in range(0, 64):
        cv.SetImageROI(img, (int(12.5 * xPos), 0, 800, 480))
        cv.Set(img, xPos * 255 / 63)
        cv.ResetImageROI(img)
    return img


def createCheckBoardPattern(isReserved=False):
    img = createImg(1)
    boolColor = True
    numsX = 4
    numsY = 4
    pixsX = 800 / numsX
    pixsY = 480 / numsY
    for x in range(0, numsX):
        for y in range(0, numsY):
            cv.SetImageROI(img, (x * pixsX, y * pixsY, (x + 1) * pixsX, (y + 1) * pixsY))
            boolColor = not (x % 2) ^ (y % 2) ^ isReserved
            cv.Set(img, 255 * boolColor)
            cv.ResetImageROI(img)
    return img


def createStardardImage():
    img = createImg()
    pixs = 800. / 7
    for i in range(0, 7):
        cv.SetImageROI(img, (int(i * pixs), 0, int(i * pixs + pixs), 480))
        cv.Set(img, stardardColors[i])
        cv.ResetImageROI(img)
    return img


if __name__ == '__main__':
    print 'Start Gen Test Screen Files ...'
    saveImageFile('red', createOneColorImage(colorRed))
    saveImageFile('green', createOneColorImage(colorGreen))
    saveImageFile('blue', createOneColorImage(colorBlue))
    saveImageFile('white', createOneColorImage(colorWhite))
    saveImageFile('black', createOneColorImage(colorBlack))
    saveImageFile('64gray', create64GrayImage())
    saveImageFile('checkboard Pattern', createCheckBoardPattern())
    saveImageFile('checkboard Pattern(inverted)', createCheckBoardPattern(True))
    saveImageFile('standard', createStardardImage())
    print 'Generate Success!'
