from django.shortcuts import render
from django.http import HttpResponse
from . import assetUtils
from .forms import uploadicon
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.

def home(request):

    args = {}
    if request.method == 'POST' and request.FILES['iconimg']:
        print(request.POST['csrfmiddlewaretoken'])
        category = request.POST['category']
        tags = request.POST['tags']
        file = request.FILES['iconimg']

        tagList = assetUtils.string2list(tags)  # Creates a list of tags with comma and removes all white spaces and empty tags.
        upload = assetUtils.addNewAsset(file, category, tagList)

        if upload:
            args['status'] = 'File Uploaded Successfully'

        else:
            args['status'] = 'There was a Problem uploading the file'

        return JsonResponse(args, safe=False)

    else:

        assets = assetUtils.getAllAssets()

        args = {
            'assets': assets,
            'iconForm': uploadicon()
        }

        return render(request, 'home.html', args)


def icons(request):

    imgType = 'icons'
    if request.method == 'POST' and request.FILES['iconimg']:

        category = request.POST['category']
        iconfile = request.FILES['iconimg']

        assetUtils.saveImg(iconfile, imgType, category)

    srcpath = os.path.dirname(__file__)
    iconrepo = assetUtils.getImages(srcpath, imgType)

    args = {
        'assetName': imgType,
        'imgrepo': iconrepo,
        'iconForm': uploadicon()
    }

    return render(request, 'index.html', args)


def illustrations(request):

    imgType = 'illustrations'
    if request.method == 'POST' and request.FILES['iconimg']:

        category = request.POST['category']
        iconfile = request.FILES['iconimg']

        assetUtils.saveImg(iconfile, imgType, category)

    srcpath = os.path.dirname(__file__)
    ilstrepo = assetUtils.getImages(srcpath, imgType)

    args = {
        'assetName': imgType,
        'imgrepo': ilstrepo,
        'iconForm': uploadicon()
    }

    return render(request, 'index.html', args)


def uploadFile(request):

    if request.method == 'POST' and request.FILES['iconimg']:
        category = request.POST['category']
        tags = request.POST['tags']
        file = request.FILES['iconimg']

        tagList = assetUtils.string2list(tags)  # Creates a list of tags with comma and removes all white spaces and empty tags.

        assetUtils.addNewAsset(file, category, tagList)

    return HttpResponse('Success')


def test(request):

    return render(request, 'test.html')


def getTags(request, string):

    tagList = assetUtils.getTags(string)
    return JsonResponse(tagList, safe=False)


def getAssets(request, taglist=None):

    assets = []
    if request.method == "GET":

        if taglist is None:
            assets = assetUtils.getAllAssets()

        else:
            new_tags = assetUtils.string2list(taglist)
            assets = assetUtils.getAssetsForTags(new_tags)

    return JsonResponse(assets, safe=False)


@csrf_exempt
def deleteAsset(request):
    x = request.body
    y = json.loads(x.decode("utf-8"))

    if request.method == "POST" and request.user.is_authenticated:
        data = {}

        status = assetUtils.delete(y['assetName'])

        if status:
            data = {
                'status': 1,
                'assetID': y['assetName'],
                'message': 'Asset Removed Successfully!'
            }

        else:
            data = {
                'status': 0,
                'assetID': y['assetName'],
                'message': 'Cannot remove the request file'
            }

    else:
        data = {
            'status': 0,
            'assetID': y['assetName'],
            'message': 'Access Denied! You do not have permission to perform this action'
        }

    return JsonResponse(data, safe=False)



# def deletefiles(request): FUNCTION TO DELETE UNNECESSARY FILES FROM THE REPOSITORY
#
#     dir = os.path.join(BASE_DIR, 'Assets', 'static', 'assets', 'images', 'icon')
#     DBList = Asset.objects.values_list('assetName', 'extension')
#     list = []
#
#     for asset in DBList:
#         list.append(asset[0] + '.' + asset[1])
#
#     fileslist = os.listdir(dir)
#     print(str(fileslist.__len__()) + ' - ' + str(list.__len__()))
#
#     for l in list:
#
#         if l in fileslist:
#             fileslist.remove(l)
#
#     for file in fileslist:
#         os.remove(os.path.join(dir,file))
#         print('File ' + file + ' deleted!')
#
#     return JsonResponse(fileslist, safe=False)

def bulkadd(request):

    files = assetUtils.test()

    test = {
        'test': 'test'
    }

    return JsonResponse(test, safe=False)


