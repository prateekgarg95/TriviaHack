from PIL import Image
import pytesseract
import cv2
import os
import search
import pprint
import webbrowser
import json

num_options = 4

os.system("adb exec-out screencap -p > screen.png")

# load the example image and convert it to grayscale
image = cv2.imread('/Users/prateekgarg95/Desktop/TriviaHack/screen.png')

# crop
image = image[300:1400, 0:1080]

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Image", gray)

# check to see if we should apply thresholding to preprocess the
# image
gray = cv2.threshold(gray, 0, 255,
                     cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(Image.open(filename)).encode('utf-8')
os.remove(filename)
print(text)

content = text.split('\n')
indexList = [i for i, s in enumerate(content) if '?' in s]
index = indexList[0]
question = ''

for i in range(0, index + 1):
    question = question + ' ' + content[i]
print question.strip()

remove_words = json.loads(open("settings.json").read())["remove_words"]
negative_words = json.loads(open("settings.json").read())["negative_words"]


def simplify_question(complex_question):
    neg = False
    qwords = complex_question.lower().split()
    if [i for i in qwords if i in negative_words]:
        neg = True
    cleanwords = [word for word in qwords if word.lower() not in remove_words]
    temp = ' '.join(cleanwords)
    clean_question = ""
    # remove ?
    for ch in temp:
        if ch != "?" or ch != "\"" or ch != "\'":
            clean_question = clean_question + ch

    return clean_question.lower(), neg


# question, negative = simplify_question(question)
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
webbrowser.get(chrome_path).open('http://google.com/search?q='+question, new=2)

option_list = []

index = index + 1

for i in range(0, num_options):
    option = ''
    while True:
        if content[index] != '':
            option = option + " " + content[index]
            index = index + 1
            break
        index = index + 1
    option_list.append(option.strip())

print option_list

results = search.google_search(question, num=10)


score = []

for i in range(0, num_options):
    count = 0
    for result in results:
        count = count + result['title'].count(option_list[i])
        count = count + result['snippet'].count(option_list[i])
    score.append(count)


print score
# if negative:
#     print "NOT"

#print option_list[score.index(max(score))]
