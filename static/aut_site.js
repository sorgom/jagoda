
function geti(id)
{
    return document.getElementById(id);
}

function debug(...args)
{

    console.log(...args);
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

function checkLogin()
{
    debug('checkLogin');
    // if (!document.loggedIn) location.replace('/login');
    getAjax('/_loggedIn', rt => {
        if (rt !== 'YES') location.replace('/login'); 
    })
}

function whatchLogin()
{
    debug('whatchLogin')
    setInterval(checkLogin, 10000);
}

//  ============================================================
//  ## popups
//  ============================================================

function escHandler(ev)
{
    if (ev.key == 'Escape')
    {
        debug('KEY ESC');
        closePopup();
    }
}

function closePopup()
{
    debug('closePopup');
    geti('popup').style.visibility = 'hidden';
    geti('cover').style.visibility = 'hidden';
    document.body.style.overflow = 'auto';

    document.removeEventListener('keydown', escHandler);
}

function showPopup(small=false)
{
    debug('showPopup');
    let cover = geti('cover');
    let popup = geti('popup');

    if (!(cover && popup)) return;

    cover.style.height = document.documentElement.scrollHeight + 'px';
    cover.style.visibility = 'visible';
    
    let ih = window.innerHeight
    let h = Math.round(ih * 0.9);
    let s = Math.round(window.scrollY + ih * 0.03);
    popup.style.height = h + 'px';
    popup.style.top = s + 'px';
    popup.style.visibility = 'visible';

    if (small)
    {
        popup.style.left = '20%';
        popup.style.width = '60%';
    }
    else
    {
        popup.style.left = '2%';
        popup.style.width = '95%';
    }

    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', escHandler);
}

function focusForm(form)
{
    debug('focusForm');
    const it = form.querySelector('input[type="text"]');

    if (it) 
    {
        debug('input found:', it);
        it.focus();
        it.select();
        return;
    }
    for (let a of form.querySelectorAll('textarea'))
    {
        if (a.value == '')
        {
            a.focus();
            break;
        }
    }
}

function popup(route, small=false)
{
    debug('popup: ' + route);
    getAjax(route, rt => {
        let pop = geti('popup');
        if (pop)
        {
            pop.innerHTML = rt;
            showPopup(small)
            let cont = geti('popup_content');
            if (cont) cont.scrollTop = 0; 
            let pf = geti('popup_form');
            if (pf) focusForm(pf);
        }
        else debug('pc not found.')
    });
}

function submitPopup(route, route2=false)
{
    debug('submitPopup:', route, route2);
    let pf = geti('popup_form');
    if (pf)
    {
        let ok = false;
        for (let a of pf.querySelectorAll('textarea'))
        {
            if (a.value != '')
            {
                ok = true;
                break;
            }
        }
        if (!ok) 
        {
            debug('missing content');
            focusForm(pf);
            return;
        }
        postAjax(new FormData(pf), route, rt => {
            if (route2) repRoute(route2);
            else setContent(rt);
        });
    }
    else getAjax(route, rt => {
        if (route2) repRoute(route2);
        else setContent(rt);
    });
}

function popupInfo(text)
{
    let elem = geti('popup_info');
    if (elem) elem.textContent = text;
}

// relace a field by ajax return
function usePopupClick(route, elemId)
{
    debug('usePopup', elemId)
    const elem = geti(elemId);
    if (elem)
    {
        getAjax(route, rt => {
            elem.innerHTML = rt,
            closePopup();            
        });
    }
}
function usePopupSubmit(form, route, elemId)
{
    postAjax(new FormData(form), route, rt => {
        const elem = geti(elemId);
        if (elem) elem.innerHTML = rt;
        closePopup();            
    });
}

function repRoute(route)
{
    debug('repRoute', route);
    location.replace(route);
    location.reload(); 
}

function setContent(html)
{
    const ct = geti('content');
    if (ct)
    {
        ct.innerHTML = html;
        const qs = ct.querySelector('input');
        if (qs) qs.focus();
    }
    closePopup();   
}

function getGoogle()
{
    debug('getGoogle');
    let pf = geti('popup_form');
    popupInfo('translating ...');
    if (pf) postAjax(new FormData(pf), '/_google', setGoogle);
}

function setGoogle(rt)
{
    debug('setGoogle');
    let data = JSON.parse(rt);
    debug(data);
    data.forEach(a => {
        let elem = geti(a[0]);
        if (elem) {
            debug(a[0], a[1]);
            elem.value = a[1];
        }
        else debug(a[0], 'not found')
    });
    popupInfo('');
}


//  ============================================================
//  ## objects / aticles
//  ============================================================

//  ============================================================
//  ## image processing
//  ============================================================

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

// place image on image / end / rm element
function placeImg(ev)
{
    debug('placeImg');
    ev.preventDefault();
    ev.stopPropagation();
    let par = this.parentNode;
    let src = geti(ev.dataTransfer.getData('id'));
    if (!src) return;
    if (otherDragSrc(this, ev))
    {
        makeDrop(src);
    } 
    debug('id:', this.imgId);
    par.insertBefore(src, this);
    sendImgOrder(par);
}

// drop into container
function dropImg(ev)
{
    debug('dropImg');
    if (this.endElem)
    {
        this.endElem.ondrop(ev);
    }
}

function rmImg(ev)
{
    debug('rmImg');
    ev.preventDefault();
    ev.stopPropagation();
    if (otherDragSrc(this, ev)) return;
    let src = geti(ev.dataTransfer.getData('id'));
    if (!src) return;
    let par = this.parentNode;
    let imgId = src.imgId;
    let objId = par.objId;
    debug('imgId:', imgId);
    debug('objId:', objId);
    if (imgId && objId)
    {
        let fd = new FormData();
        fd.set('imgId', imgId);
        fd.set('objId', objId);
        postAjax(fd, '/_rmObjImg', rt => {
            --par.currNumImgs;
            par.removeChild(src);
            sendImgOrder(par);
            markExceed(par);
            reloadUnusedImgs();
        })
    }
}

function dragOver(ev)
{
    ev.preventDefault();
}

function makeDrop(elem)
{
    elem.ondrop = placeImg;
    elem.ondragover = dragOver;
}

function makeImg(target, e, drop)
{
    let d = document.createElement('div');
    if (drop) makeDrop(d);
    d.id = [target.id, e['ID']].join('_');
    d.imgId = e['ID'];
    d.ord = e['ORD'];
    debug('ID:', d.id);
    let i = document.createElement('img');
    i.src = e['SRC'];
    i.draggable = true;
    i.ondragstart = dragImg;
    i.onclick = imgInfo;
    d.appendChild(i);
    return d;
}

// put at end position field and element deleter
function addImgEnd(target)
{
    debug('addImgEnd');
    let de = document.createElement('div');
    de.ondrop = placeImg;
    de.ondragover = dragOver;
    de.className = 'imgend';
    de.innerHTML = '@END';
    target.appendChild(de);

    target.endElem = de;
    target.ondrop = dropImg;
    target.ondragover = dragOver;

    let dr = document.createElement('div');
    dr.ondrop = rmImg;
    dr.ondragover = dragOver;
    dr.className = 'imgrm';
    dr.innerHTML = 'REMOVE';
    target.appendChild(dr);
}

function removeEnd(target)
{
    debug('removeEnd')
    let nodes = [];
    target.childNodes.forEach(e => { if (!e.imgId) nodes.push(e); });
    nodes.forEach(e => { target.removeChild(e); });
}

function upateImgs(target, json, drop)
{
    if (target)
    {
        debug('upateImgs');
        removeEnd(target);
        const ret = JSON.parse(json);
        let cns = [];
        target.childNodes.forEach(cn => { cns.push(cn) });
        const data = ret['data'];
        data.forEach(e => {
            let eId = e['ID'];
            while ((cns.length > 0) && (cns[0].imgId < eId))
            {
                target.removeChild(cns.shift());
            }
            if (cns.length === 0)
            {
                target.appendChild(makeImg(target, e, drop));
            }
            else if (cns[0].imgId === eId)
            {
                cns.shift();
            }
            else
            {
                target.insertBefore(makeImg(target, e, drop), cns[0]);
            }
        })
        cns.forEach(cn => { target.removeChild(cn); });
        if (drop) addImgEnd(target);
        target.maxNumImgs = ret['max'];
        markExceed(target);
    }
}

function loadObjImgs(trgId, id)
{
    debug('loadObjImgs:', id);
    let target = geti(trgId);
    if (target)
    {
        target.objId = id;
        getAjax('/_objImgs/' + id, rt => { 
            upateImgs(target, rt, true);
        });
    }
}

function uploadImgs(inp, trgId, id)
{
    debug('uploadImgs:', id);
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
    postAjax(fd, '/_addObjImgs/' + id, rt => {
        upateImgs(target, rt, true);
    });
}

function loadUnusedImgs(trgId)
{
    debug('loadUnusedImgs:', trgId);
    let target = geti(trgId);
    if (target)
    {
        document.unusedImgsContainer = target;
        reloadUnusedImgs();
    }
}

function reloadUnusedImgs()
{
    debug('reloadUnusedImgs');
    let target = document.unusedImgsContainer;
    if (target)
    {
        getAjax('/_unusedImgs', rt => {
            upateImgs(target, rt, false);
        });
    }
}

function setExceeded(elem, exceeded)
{
    if (exceeded) elem.classList.add('exd');
    else elem.classList.remove('exd');
}

function markExceed(target)
{
    debug('markExceed');
    let n = 1;
    target.childNodes.forEach(e => {
        if (e.imgId)
        {
            setExceeded(e, (target.maxNumImgs && (n > target.maxNumImgs)));
            ++n; 
        }
    })
    updateObjImg();
}

function sendImgOrder(target)
{
    let objID = target.objId;
    if (objID)
    {
        debug('sendImgOrder:', objID);
        let chg = [];
        let n = 0;
        target.childNodes.forEach(e => {
            if (e.imgId)
            {
                if (e.ord != n)
                {
                    chg.push([e.imgId, n]);
                    e.ord = n;
                }
                ++n; 
            }
        })
        if (chg.length > 0)
        {
            postJson(chg, '/_orderObjImgs/' + objID, rt => { 
                markExceed(target);
            });
        }

    }
}

function imgInfo()
{
    debug('imgInfo:', this.parentNode.imgId);
    popup('/_imgInfo/' + this.parentNode.imgId);
}

function updateObjImg()
{
    const img = geti('objImg');
    const oid = geti('objId');
    if (img && oid)
    {
        debug('updateObjImg ...')
        getAjax('/_objImg/' + oid.textContent, rt => {
            debug('updateObjImg:', rt)
            img.src = rt;
        })
    }
}

//  ============================================================
//  ## print
//  ============================================================

function printAjax(route)
{
    getAjax(route, printContent);
}

function printElementContentById(id)
{
    let elem = geti(id);
    if (elem) printElementContent(elem)
}

// print innerHTML of an element
// NOTE: css formatting gets lost unless explicitly given in style attributes
function printElementContent(elem)
{
    printContent(elem.innerHTML)
}

// print content
function printContent(content)
{
    const ifr = document.createElement("iframe");
    ifr.style.display = "none";
    document.body.appendChild(ifr);
    const pri = ifr.contentWindow;
    pri.document.open();
    pri.document.write(content);
    pri.document.close();
    pri.focus();
    pri.print();
    pri.onafterprint = () => { document.body.removeChild(ifr); }
}

