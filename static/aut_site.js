
function closePopup()
{
    console.log('closePopup');
    document.getElementById('popup').style.visibility = 'hidden';
    document.getElementById('cover').style.visibility = 'hidden';
    document.body.style.overflow = 'auto';
}

function showPopup()
{
    console.log('showPopup');
    var cover = document.getElementById('cover');
    cover.style.height = document.documentElement.scrollHeight + 'px';
    cover.style.visibility = 'visible';

    var popup =  document.getElementById('popup');
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
    console.log('popup: ' + route);

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if (this.readyState == XMLHttpRequest.DONE  && this.status == 200) 
        {
            console.log('ajax return');
            document.getElementById('popup_content').innerHTML = this.responseText;
            showPopup()
            var areas = document.getElementById('popup_form').querySelectorAll('textarea');
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
    console.log('processPopup: ' + route);

    var form = document.getElementById('popup_form');
    if (form.querySelector(':invalid'))
    {
        console.log('no content!');
        return false;
    }

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if (this.readyState == XMLHttpRequest.DONE  && this.status == 200) 
        {
            console.log('ajax return');
            document.getElementById('content').innerHTML = this.responseText;
            closePopup()
        }
    };

    var data = new FormData(form);
    xhr.open('POST', route, true);
    xhr.send(data);
    return false;
}

function uploadFiles(inp, route)
{
    console.log('uploadFiles: ' + route);
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if (this.readyState == XMLHttpRequest.DONE  && this.status == 200) 
        {
            console.log('ajax return');
            let r = document.getElementById('result');
            while (r.firstChild)
            {
                r.removeChild(r.firstChild);
            }

            let data =  JSON.parse(this.responseText)
            for (let n in data)
            {
                console.log(data[n]);
                let e = data[n];
                let i = document.createElement('img');
                i.src = e['src'];
                i.ord = e['ord'];
                let d = document.createElement('div');
                d.appendChild(i);
                r.appendChild(d);
            }
            inp.value = null;
        }
    };

    let fd  = new FormData();
    let num =  inp.files.length;
    for (let n = 0; n < num; ++n)
    {
        fd.append('files', inp.files[n])
    }
    xhr.open('POST', route, true);
    xhr.send(fd);
}