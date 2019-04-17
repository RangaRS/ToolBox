import os, shutil, time
from MDMRepository.settings import BASE_DIR, MEDIA_ROOT

from django.core.files.storage import FileSystemStorage
from .models import Tags, Asset
from collections import OrderedDict
from operator import itemgetter

def string2list(text):
    listItems = [x.strip() for x in text.split(',') if x.strip()]
    return listItems


def removeDuplicatesFromList(lists):
    return list(OrderedDict.fromkeys(lists))


def getFolders(path):
    folders = []
    for r, d, f in os.walk(path):
        # print(r)
        if os.path.isdir(r):
            folders.append(r)

    return folders


def getImages(path, folder):
    data = {}
    srcPath = path + '/static/assets/' + folder

    folders = getFolders(srcPath)
    # print(folders)

    for folder in folders:
        svgfiles = []
        files = os.listdir(folder)

        for file in files:
            if file.endswith('.svg'):
                svgfiles.append(file)

        if len(svgfiles) is not 0:
            if folder is srcPath:
                data['misc'] = svgfiles

            else:
                foldername = folder[len(srcPath) + 1:]
                data[foldername] = svgfiles

    return data


def saveImg(newFile, fileName, Category):
    savDir = os.path.join(BASE_DIR, 'Assets', 'static', 'assets', 'images', Category)

    fs = FileSystemStorage()
    filename = fs.save(fileName, newFile)
    srcDir = MEDIA_ROOT + '/' + filename

    if os.path.isfile(srcDir):

        if not os.path.isdir(savDir):
            os.makedirs(savDir)

        moveFile = shutil.copy(srcDir, savDir)
        os.unlink(srcDir)

        print('File copied to folder successfully!')

    else:
        moveFile = None

    if os.path.isfile(moveFile):
        return True

    else:
        return False


def updateTagList(TagList):
    tagID = []

    for tag in TagList:
        tag = tag.strip().lower()
        print(tag)

        try:
            getTag = Tags.objects.get(tagName=tag)
            tagID.append(getTag)

        except:
            newTag = Tags(tagName=tag)
            newTag.save()
            tagID.append(newTag)

    return tagID


def addNewAsset(File, Category, TagList):
    newAsset = Asset()
    newAsset.save()

    fileName = str(time.time()) + str(newAsset.pk)
    fileName = fileName.replace('.', '')

    fileExt = File.name.rsplit('.', 1)
    fileExt = fileExt[1]

    assetTags = updateTagList(TagList)

    newAsset.assetName = fileName
    newAsset.extension = fileExt
    newAsset.assetType = Category

    for tag in assetTags:
        newAsset.tags.add(tag)
    newAsset.save()

    fullname = fileName + '.' + fileExt

    saveFile = saveImg(File, fullname, Category)

    if saveFile:
        return True


def getTags(value):

    try:
        tagList = Tags.objects.filter(tagName__icontains=value)

        tagNames = []
        for tag in tagList:
            tagname = tag.tagName
            tagNames.append(tagname)

    except:
        tagNames = ['None']

    return tagNames


def getAssetsForTags(tags):

    uniqueTags = removeDuplicatesFromList(tags)

    uniqueAssets = []
    tagNassets = {}
    assetNscore = {}
    finalassets = []

    for tag in uniqueTags:

        assetObjs = Asset.objects.filter(tags=tag)
        uniqueAssets = uniqueAssets + list(assetObjs)
        tagNassets[tag] = list(assetObjs)

    uniqueAssets = set(uniqueAssets)

    for asset in uniqueAssets:
        score = 1

        for tag,assetlist in tagNassets.items():

            if asset in assetlist:
                score = score + 1

        assetNscore[asset.assetName] = score

    assetsByScore = sorted(assetNscore.items(), key=itemgetter(1))

    for x in reversed(assetsByScore):
        finalassets.append(x[0])

    return finalassets


def getAllAssets(type=None):

    if type is None:
        assets = Asset.objects.all().order_by('-addedOn').values_list('assetName', flat=True)

    else:
        assets = Asset.objects.filter(assetType=type).order_by('-addedOn').values_list('assetName', flat=True)

    return list(assets)


def delete(assetName):

    try:
        asset = Asset.objects.get(assetName=assetName)
        assetName = asset.assetName
        assetType = asset.assetType
        extn = asset.extension

        fileDir = os.path.join(BASE_DIR, 'Assets', 'static', 'assets', 'images', assetType, assetName + '.' + extn)

        if os.path.isfile(fileDir):
            try:
                os.remove(fileDir)
                asset.delete()
                return True

            except:
                print('problem deleting file!')
                return False

        else:
            return False

    except:
        return False


def test():
    rootpath = '/Users/sree-3791/MDMRepository/Assets/static/assets/icons/Status'
    fileExt = 'svg'
    category = 'icon'

    files = os.listdir(rootpath)

    for file in files:

        if file.endswith('.svg'):
            newAsset = Asset()
            newAsset.save()

            TagList,fileName = file.split('|')
            filePath = os.path.join(rootpath, file)
            saveName = str(time.time()) + str(newAsset.pk)
            saveName = fileName.replace('.', '')
            savePath = os.path.join(os.path.join(BASE_DIR, 'Assets', 'static', 'assets', 'images', category, saveName + '.svg'))

            tags = string2list(TagList)
            assetTags = updateTagList(tags)

            newAsset.assetName = saveName
            newAsset.extension = fileExt
            newAsset.assetType = category

            for tag in assetTags:
                newAsset.tags.add(tag)
            newAsset.save()

            moveFile = shutil.copy(filePath, savePath)

            if os.path.isfile(moveFile):
                print('file copied successfully!')

            else:
                print('Problem adding the asset')
                newAsset.delete()

