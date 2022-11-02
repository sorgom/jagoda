
function closeModal(id)
{
    console.log('closeModal');
    document.getElementById(id).style.visibility = "hidden";
    document.getElementById('cover').style.visibility = "hidden";
    document.body.style.overflow = 'auto';
}

function showModal(id)
{
    console.log('showModal');
    cover = document.getElementById('cover');
    cover.style.height = document.documentElement.scrollHeight + 'px';
    cover.style.visibility = "visible";
    var elem =  document.getElementById(id);
    var h = Math.round(window.innerHeight / 2.0);
    var s = window.scrollY + h / 2;
    elem.style.height = h + 'px';
    elem.style.top = s + 'px';
    elem.style.visibility = "visible";
    document.body.style.overflow = 'hidden';
}

function loadDemo()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange=function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            document.getElementById("mod_content").innerHTML = this.responseText;
        }
    };
    xhttp.open('GET', '/demolist', true);
    xhttp.send();
    showModal('modal');
}

function wumpel(id)
{
    closeModal('modal')
}

function ajaxForm(frmID, trgID)
{
    console.log('ajaxForm');

    var label = "got response: ";

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function()
    {
        if (this.readyState == XMLHttpRequest.DONE  && this.status == 200) 
        {
            console.log(label + this.responseText);
            // document.getElementById("mod_content").innerHTML = this.responseText;
        }
    };

    var form = document.getElementById(frmID);

    var data = new FormData(form);
    // var data = new FormData();
    // data.append('en', 'person');
    // data.append('fr', 'password');
    // data.append('de', 'place');
    // data.append('hr', 'key');

    xhr.open('POST', '/ajaxform', true);
    // xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(data);
}