
export const SEND_TEXT_AI = 'SEND_TEXT_AI'



export function sendTextAi(text, model) {
    return {
        type: SEND_TEXT_AI,
        payload: {
            text : text,
            model : model
        }
    }

}

