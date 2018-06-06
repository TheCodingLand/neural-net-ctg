import { call, put } from 'redux-saga/effects'

let hostname =window.location.hostname.split('.')[-2] + "." + window.location.hostname.split('.')[-1]
console.log(hostname)

export function* chat_api(text) { 
    const response= yield call(
        fetch,`http://ai-api.${hostname}/chat`,
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
        fetch,`http://ai-api.${hostname}/updatebrain`,
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

