import { call, put } from 'redux-saga/effects'
function* Api(text) { 
    const response= yield call(
        fetch,'http://julien.tech:5005',
        {
        body: JSON.stringify({text:text}),
        method:'POST',
        headers: {
            'content-type': 'application/json'
          },
          mode: 'cors', // no-cors, cors, *same-origin
    } )

    let result = yield response.json()
    result = result.results
return result
}

export default Api