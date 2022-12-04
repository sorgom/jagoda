function db(...args)
{
    console.log(...args);
}

//  close a pulldown element
function closeDrop(elem)
{
    elem.classList.remove('show');
}

function toggleDrop(elem)
{
    elem.classList.toggle('show')
    if (elem.classList.contains('show')) closeOtherDrops(elem);
}

function initDropdown(pd)
{
    let a = pd.querySelector('a');
    let d = pd.querySelector('div').querySelector('div')

    if (a && d)
    {
        a.onclick =  () => { toggleDrop(d); }
        a.classList.add('dropbtn')
        d.classList.add('dropcont')
    }
}

function getDropdowns(what='div.dropdown')
{
    let m = document.getElementById('menu');
    if (!m) return [];
    return m.querySelectorAll(what)
}

function closeOtherDrops(elem)
{
    let dds = getDropdowns('.dropcont');
    dds.forEach(dd => {
        if (dd != elem) closeDrop(dd);
    })
}

function initDropdowns()
{
    db('initDropdowns')
    let dds = getDropdowns();
    db('dds', dds.length)
    dds.forEach(initDropdown);
}

initDropdowns();

window.onclick = function(event) 
{
    if (!event.target.matches('.dropbtn'))
    {
        let dds = getDropdowns('.dropcont');
        dds.forEach(dd => { closeDrop(dd) })
    }
}