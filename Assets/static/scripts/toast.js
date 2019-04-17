function toastMsg(status, message, timeout){
    var container = document.createElement('DIV');
    var img = document.createElement('IMG');
    var msg = document.createElement('SPAN');
    var body = document.getElementById('docBody');

    img.className = 'statusIcon';
    msg.className = 'statusMsg';
    msg.innerHTML = message;

    if (status==200){
        container.className = 'toast success';
        img.setAttribute('src', '/static/images/success.svg');
    }

    else if(status==300){
        container.className = 'toast info';
        img.setAttribute('src', '/static/images/info.svg');
    }

    else if(status==400){
        container.className = 'toast alert';
        img.setAttribute('src', '/static/images/alert.svg');
    }

    else if(status==500){
        container.className = 'toast error';
        img.setAttribute('src', '/static/images/error.svg');
    }

    else {
        container.className = 'toast info';
        img.setAttribute('src', '/static/images/info.svg');
    }

    container.appendChild(img);
    container.appendChild(msg);
    container.style.bottom = '30px';
    container.style.opacity = '0';

    body.appendChild(container);

    container.onload = setTimeout(function(){
        container.style.bottom = null;
        container.style.opacity = null;
    }, 200);

    setTimeout(function(){
        container.parentNode.removeChild(container);
    }, 4000);
}