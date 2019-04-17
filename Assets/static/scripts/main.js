    function scrolltobox(el) {
        var text = el.getAttribute('data-tab');
        var boxes = document.getElementsByClassName('box');

        for (var i=0; i < boxes.length; i++) {
            var tabtext = boxes[i].getAttribute('data-tab-body');

            if (tabtext == text) {
                window.scrollTo(0, boxes[i].offsetTop - 60);
                document.getElementsByClassName('active')[0].classList.remove('active');
                el.classList.add('active');
                break;
            }
        }
    };

    function stopPageLoader() {
        document.getElementById('pageLoader').style.height = '0px';

        window.setTimeout(function(){
            document.getElementById('pageLoader').remove();
        }, 300);
    }

    window.onload = function() {
        stopPageLoader();
    }

    /* =============== UI RELATED JS ENDS HERE ================= */


    function getCSRF() {
        var cookies = document.cookie.split(';');

        cookies.forEach(function(el){

            if (el.indexOf("csrftoken") >= 0) {
                var token = el.split('=');
                var csrf = token[1];
                console.log(csrf);
                return csrf;
            }

        });
    }

    function AJAX(request, url, data, callback, getscrf) {

        var csrf;
        var xhttp = new XMLHttpRequest();

          xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                callback(this.responseText);
            }
          };

          if (request=="POST" && data!=null){

            xhttp.open(request, url);
//            xhttp.setRequestHeader('X-CSRFToken', getCSRF());
            xhttp.send(JSON.stringify(data));
          }

          else{
            xhttp.open(request, url + data);
            xhttp.send();
          }
        }

    function getTagList(id) {

      if (id.value == ''){
        var container = document.getElementById("tagListContainer");
        removeInnerChilds(container);
        container.style.display = 'none';

      }

      else {
        var req = AJAX("GET", "/getTags/", id.value, showAvailableTags, getCSRF);
      }
    }

    function showAvailableTags(tagList) {
        var data = JSON.parse(tagList);
        var container = document.getElementById("tagListContainer");
        container.style.display = 'inline-block';

        removeInnerChilds(container);

        data.forEach(function(el) {
            var span = document.createElement("SPAN");
            span.innerHTML = el;
            span.className = "tagItem";
            span.setAttribute("onclick", "addTag(this)");
            container.appendChild(span);
        });
    }

    function removeInnerChilds(el){
        while (el.firstChild) {
            el.removeChild(el.firstChild);
        }
    }


    function addTag(el) {
        var container = document.getElementById("searchbarcontainer");
        var searchfield = document.getElementById("tagSearch");
        var newTag = document.createElement("SPAN");

        newTag.innerHTML = el.innerHTML;
        newTag.className = "selectedTag";
        newTag.setAttribute("onclick", "removeTag(this)");

        container.insertBefore(newTag, searchfield);

        getAssetByTags(document.getElementById("searchbarcontainer"));
    }


    function removeTag(el) {
        el.remove();
        getAssetByTags(document.getElementById("searchbarcontainer"));
    }


    function getAssetByTags(el){
        var tagList = el.getElementsByClassName("selectedTag");
        var tags = [];

        [].forEach.call(tagList, function(el) {
            var tagName = el.innerHTML;
            tags.push(tagName);
        });

        if (tags == 'undefined'){
            tags = '*';
        }

        var req = AJAX("GET", "/getAssets/", tags, populateAssets, getCSRF);
    }


    function populateAssets(data){
        var imgs = JSON.parse(data);
        var containerbody = document.getElementById('previewicons');

        removeInnerChilds(containerbody);

        imgs.forEach(function(el) {
            var string = '<div style="transform:scale(0);" id="A'+el+'" class="iconContainer"><div class="actions"><a class="iconAnchor" href="/static/assets/images/icon/'+ el +'.svg" download="'+ el +'"> <img class="download" data-model-name="'+ el +'" src="/static/images/download.svg"></a> <img class="edit" data-model-name="'+el+'" onclick="copyImg(this)" src="/static/images/copy.svg"> <img class="delete" data-model-name="'+el+'" onclick="deleteAsset(this)" src="/static/images/delete.svg"></div><img src="/static/assets/images/icon/'+el+'.svg"></div>'

            containerbody.innerHTML += string;

            setTimeout(function(){
                document.getElementById('A'+el).style.transform = null;
            }, 100);
        });

    }

    function deleteAsset(el) {
        var x = el.getAttribute('data-model-name');
        var data = {
            'assetName': x,
            'status': 'dummy status',
            'something': 5
        }

        var req = AJAX("POST", "/deleteAsset/", data, deleteStatus, getCSRF)
    }

    function deleteStatus(el) {
        var data = JSON.parse(el);

        if (data.status == 1){
            element = document.getElementById('A' + data.assetID)
            element.parentNode.removeChild(element);
            toastMsg(200, data.message);
        }

        else {
            toastMsg(500, data.message);
        }
    }

    function hideWindow() {
        var x = document.getElementById('sideWindow');
        x.style.display = 'none';
    }

    function showUploadForm() {
        var x = document.getElementById('sideWindow');
        x.style.display = 'block';
    }

//    function submitForm(el) {
//        var form = document.getElementById(el);
//        var fd = new FormData(form);
//        console.log(fd);
//        var req = AJAX("POST", "", fd, uploadAsset)
//    }

    function uploadAsset(el){
        var data = JSON.parse(el);
        console.log(data);
    }

    function copyImg(el){
      var img = '';
      var y = el.getAttribute('data-model-name');
      var x = document.getElementById('A' + y);
      var imgsrc = x.children;
      for(i=0; i<imgsrc.length; i++) {
        if(imgsrc[i].tagName == 'IMG'){
            img = imgsrc[i];
            break;
        }
      }

        var div = document.getElementById('DivtoCopy');
        img.contentEditable = 'true';
        var controlRange;
        if (document.body.createControlRange) {
        controlRange = document.body.createControlRange();
        controlRange.addElement(img);
        controlRange.execCommand('Copy');
        }
        img.contentEditable = 'false';

    }
