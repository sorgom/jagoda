
function geti(id)
{
    return document.getElementById(id);
}

function debug(str)
{
    console.log(str);
}

function closePopup()
{
    debug('closePopup');
    geti('popup').style.visibility = 'hidden';
    geti('cover').style.visibility = 'hidden';
    document.body.style.overflow = 'auto';
}

function showPopup()
{
    debug('showPopup');
    var cover = geti('cover');
    cover.style.height = document.documentElement.scrollHeight + 'px';
    cover.style.visibility = 'visible';

    var popup =  geti('popup');
    var ih = window.innerHeight
    var h = Math.round(ih * 0.8);
    var s = Math.round(window.scrollY + ih * 0.1);
    popup.style.height = h + 'px';
    popup.style.top = s + 'px';
    popup.style.visibility = 'visible';
    document.body.style.overflow = 'hidden';
}

function popup(route)
{
    debug('popup: ' + route);

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if (this.readyState == XMLHttpRequest.DONE  && this.status == 200) 
        {
            debug('ajax return');
            geti('popup_content').innerHTML = this.responseText;
            showPopup()
            var areas = geti('popup_form').querySelectorAll('textarea');
            for (var a of areas)
            {
                if (a.value == '')
                {
                    a.focus();
                    break;
                }
            }
        }
    };

    xhr.open('GET', route, true);
    xhr.send();
}

function submitPopup(route)
{
    debug('processPopup: ' + route);

    var form = geti('popup_form');
    if (form.querySelector(':invalid'))
    {
        debug('no content!');
        return false;
    }

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if (this.readyState == XMLHttpRequest.DONE  && this.status == 200) 
        {
            debug('ajax return');
            geti('content').innerHTML = this.responseText;
            closePopup()
        }
    };

    var data = new FormData(form);
    xhr.open('POST', route, true);
    xhr.send(data);
    return false;
}

function dragImg(ev)
{
    debug('dragImg');
    ev.dataTransfer.setData('text', ev.target.parentNode.id);
}

function dropImg(ev)
{
    debug('dropImg');
    ev.preventDefault();
    let srcid = ev.dataTransfer.getData('text');
    let src = geti(srcid);
    debug('src: ' + src);
    node = ev.target.tagName.toLowerCase() === 'img' ? ev.target.parentNode : ev.target;
    debug('node: ' + node.tagName);
    debug('id  : ' + node.imgId);
    let par = node.parentNode;
    par.insertBefore(src, node);
    sendImgOrder(par);
}

function dragOverImg(ev)
{
    // debug('dragOverImg');
    ev.preventDefault();
}

function clean(target)
{
    while (target.firstChild)
    {
        target.removeChild(target.firstChild);
    }
}

function addImg(target, e)
{
    let d = document.createElement('div');
    d.ondrop = dropImg;
    d.ondragover = dragOverImg;
    d.id = target.id + '_img_' + e['id'];
    d.imgId = e['id'];
    d.ord = e['ord'];
    debug('imgId: ' + d.id);
    // d.innerHTML = d.imgId;

    let i = document.createElement('img');
    i.src = e['src'];
    i.draggable = true;
    i.ondragstart = dragImg;
    d.appendChild(i);
    target.appendChild(d);
}

function endId(target)
{
    return target.id + '__END';
}

function addEnd(target)
{
    debug('addEnd');
    let d = document.createElement('div');
    d.ondrop = dropImg;
    d.ondragover = dragOverImg;
    d.className = 'imgend';
    d.innerHTML = 'END';
    d.id = endId(target);
    target.appendChild(d);
}

function removeEnd(target)
{
    end = geti(endId(target));
    if (end)
    {
        target.removeChild(geti(endId(target)));
    }
}

function displayImages(target, json)
{
    debug('displayImages');
    clean(target);
    addImgs(target, json);
}

function addImgs(target, json)
{
    debug('addImgs');
    const data = JSON.parse(json);
    removeEnd(target);
    data.forEach(e => { addImg(target, e); });
    addEnd(target);
}


function postAjax(fdata, route, func)
{
    debug('postAjax: ' + route);
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function()
    {
        if (this.readyState == XMLHttpRequest.DONE  && this.status == 200) 
        {
            debug('postAjax return');
            func(this.responseText);
        }
    };
    xhr.open('POST', route, true);
    xhr.send(fdata);
}

function getAjax(route, func)
{
    debug('getAjax: ' + route);
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function()
    {
        if (this.readyState == XMLHttpRequest.DONE  && this.status == 200) 
        {
            debug('getAjax return');
            func(this.responseText);
        }
    };
    xhr.open('GET', route, true);
    xhr.send();
}

function loadImages(trgId, id)
{
    debug('loadImages: ' + id);
    let target = geti(trgId);
    if (target)
    {
        target.objId = id;
        target.loaded = true;
        getAjax('/_imgs/' + id, rt => { displayImages(target, rt); });
    }
}

function uploadImages(inp, trgId, id)
{
    debug('uploadImages: ' + id);
    let fd  = new FormData();
    let num = inp.files.length;
    for (let n = 0; n < num; ++n)
    {
        fd.append('files', inp.files[n])
    }
    postAjax(fd, '/_addimgs/' + id, rt => {
        let target = geti(trgId);
        if (target)
        {
            addImgs(target, rt);
        }
        inp.value = null;
    });
}

function sendImgOrder(target)
{
    let objID = target.objId;
    if (objID)
    {
        debug('sendImgOrder: ' + objID);
        let chg = [];
        let n = 0;
        target.childNodes.forEach(e => {
            let imgId  = e.imgId;
            let ord = e.ord;
            if (imgId && ord != n)
            {
                debug('imgId: ' + imgId);
                chg.push([imgId, n]);
                e.ord = n;
            }
            ++n; 
        })
        if (chg.length > 0)
        {
            const js = JSON.stringify(chg);
            debug('json: ' + js);
            let fd = new FormData();
            fd.set('json', js);
            postAjax(fd, '/_orderimgs/' + objID, rt => {
            });
        }
    }
}