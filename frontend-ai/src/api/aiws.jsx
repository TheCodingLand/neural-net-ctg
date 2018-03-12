import { call, put } from 'redux-saga/effects'
export function* chat_api(text) { 
    const response= yield call(
        fetch,'http://julien.tech:5005/api/chat',
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


export function* update_brain_api(text) { 
    const response = yield call(
        fetch,'http://julien.tech:5005/api/predict',
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

