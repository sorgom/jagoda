
function geti(id)
{
    return document.getElementById(id);
}

function debug(str)
{
    console.log(str);
}

function clean(target)
{
    while (target.firstChild)
    {
        target.removeChild(target.firstChild);
    }
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

function postJson(data, route, func)
{
    const js = JSON.stringify(data);
    debug('json: ' + js);
    let fd = new FormData();
    fd.set('json', js);
    postAjax(fd, route, func);
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
    getAjax(route, rt => {
        let pc = geti('popup_content');
        let pf = geti('popup_form');
        if (pc && pf)
        {
            pc.innerHTML = rt;
            showPopup()
            for (let a of pf.querySelectorAll('textarea'))
            {
                if (a.value == '')
                {
                    a.focus();
                    break;
                }
            }
        }
    });
}

function submitPopup(route)
{
    debug('submitPopup: ' + route);
    let form = geti('popup_form');
    if  (!form) return;
    if (form.querySelector(':invalid'))
    {
        debug('missing content');
        return;
    }
    postAjax(route, new FormData(form), rt => {
        let ct = geti('content');
        if (ct) ct.innerHTML = rt;
        closePopup();
    });
}

function dragImg(ev)
{
    debug('dragImg');
    ev.dataTransfer.setData('id',  this.parentNode.id);
    ev.dataTransfer.setData('par', this.parentNode.parentNode.id);
}

function otherDragSrc(node, ev)
{
    let parid = ev.dataTransfer.getData('par');
    return parid !== node.parentNode.id;
}

function placeImg(ev)
{
    debug('placeImg');
    ev.preventDefault();
    if (otherDragSrc(this, ev)) 
    {
        // TODO: handle drag from other selection
        return;
    }
    let src = geti(ev.dataTransfer.getData('id'));
    if (!src) return;
    debug('src: ' + src);
    debug('id  : ' + this.imgId);
    let par = this.parentNode;
    par.insertBefore(src, this);
    sendImgOrder(par);
}

function rmImg(ev)
{
    debug('rmImg');
    ev.preventDefault();
    if (otherDragSrc(this, ev)) return;
    let src = geti(ev.dataTransfer.getData('id'));
    if (!src) return;
    let par = this.parentNode;
    let imgId = src.imgId;
    let objId = par.objId;
    debug('imgId: ' + imgId);
    debug('objId: ' + objId);
    if (imgId && objId && confirm('remove image?'))
    {
        let fd = new FormData();
        fd.set('imgId', imgId);
        fd.set('objId', objId);
        postAjax(fd, '/_rmimg', rt => {
            par.removeChild(src);
        })
    }
}

function dragOverImg(ev)
{
    ev.preventDefault();
}


function addImg(target, e, drop)
{
    let d = document.createElement('div');
    if (drop)
    {
        d.ondrop = placeImg;
        d.ondragover = dragOverImg;
    }
    d.id = target.id + '_' + e['id'];
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

// put at end position field
function addImgEnd(target)
{
    debug('addImgEnd');
    let de = document.createElement('div');
    de.ondrop = placeImg;
    de.ondragover = dragOverImg;
    de.className = 'imgend';
    de.innerHTML = '@END';
    target.appendChild(de);

    let dr = document.createElement('div');
    dr.ondrop = rmImg;
    dr.ondragover = dragOverImg;
    dr.className = 'imgrm';
    dr.innerHTML = 'DEL';
    target.appendChild(dr);
}

function removeEnd(target)
{
    debug('removeEnd')
    let nodes = [];
    target.childNodes.forEach(e => { if (!e.imgId) nodes.push(e); });
    nodes.forEach(e => { target.removeChild(e); });
}

function displayImages(target, json, drop)
{
    if (target)
    {
        debug('displayImages');
        clean(target);
        addImgs(target, json, drop);
    }
}

function addImgs(target, json, drop)
{
    if (target)
    {
        debug('addImgs');
        const ret = JSON.parse(json);
        const data = ret['data'];
        const msg  = ret['msg'];
        removeEnd(target);
        data.forEach(e => { addImg(target, e, drop); });
        if (drop) addImgEnd(target);
        if (msg) alert(msg);
    }
}

function loadImages(trgId, id)
{
    debug('loadImages: ' + id);
    let target = geti(trgId);
    if (target)
    {
        target.objId = id;
        getAjax('/_imgs/' + id, rt => { displayImages(target, rt, true); });
    }
}

function uploadImages(inp, trgId, id)
{
    debug('uploadImages: ' + id);
    let target = geti(trgId);
    if (!target) return;
    let objId = target.objId;
    if (!objId) target.objId = id;
    else if (objId !== id) return;

    let fd  = new FormData();
    for (let f of inp.files)
    {
        fd.append('files', f);
    }
    inp.value = null;
    postAjax(fd, '/_addimgs/' + id, rt => {
        addImgs(geti(trgId), rt, true);
    });
}

// function numImages(target)
// {
//     let objID = target.objId;
//     let n = 0;
//     if (objID)
//     {
//         target.childNodes.forEach(e => {
//             if (e.imgId) ++n;
//         })
//     }
//     return n;
// }

function sendImgOrder(target)
{
    let objID = target.objId;
    if (objID)
    {
        debug('sendImgOrder: ' + objID);
        let chg = [];
        let n = 0;
        target.childNodes.forEach(e => {
            let id  = e.imgId;
            let ord = e.ord;
            if (id && ord != n)
            {
                debug('imgId: ' + id);
                chg.push([id, n]);
                e.ord = n;
            }
            ++n; 
        })
        if (chg.length > 0)
        {
            postJson(chg, '/_orderimgs/' + objID, rt => {});
        }
    }
}