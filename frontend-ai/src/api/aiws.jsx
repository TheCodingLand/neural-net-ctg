import { call, put } from 'redux-saga/effects'
export function* chat_api(text) { 
    const response= yield call(
        fetch,'https://julien.tech/api/chat',
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


export function* update_brain_api(conversation) { 
    let convstring = conversation.map((s) => {  if (s.user != "Tina") {return s.content} })
    
    convstring = convstring.join(' ')
    console.log(convstring)
    const response = yield call(
        fetch,'https://julien.tech/api/updatebrain',
        {
        body: JSON.stringify({text:convstring}),
        method:'POST',
        headers: {
            'content-type': 'application/json'
          },
          mode: 'cors', // no-cors, cors, *same-origin
    } )
 

    let result = yield response.json()
    result = result

return result
}

