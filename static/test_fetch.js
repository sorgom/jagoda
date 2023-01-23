function debug(...args)
{

    console.log(...args);
}

async function testFetch(route, func)
{
    debug('testFetch:', route);
    const response = await fetch(route,
        {
            headers: {
                'Access-Control-Allow-Origin': route
            }
        }
        
    );
    func(response.body())
}

function fastTest()
{
    testFetch('http://127.0.0.1:8000/', debug);
}
