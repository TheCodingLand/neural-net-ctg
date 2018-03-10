
export const SEND_TEXT_AI = 'SEND_TEXT_AI'
export const PREDICTION_SUCCEDED = 'PREDICTION_SUCCEDED'
export const PREDICTION_FAILED = 'PREDICTION_FAILED'
export const PREDICTION_REQUESTED = 'PREDICTION_REQUESTED'
export const CLEAR_CHAT = 'CLEAR_CHAT'

export function predictionSucceeded(data) {
  console.log('called action on prediction success')
    return {
      type: PREDICTION_SUCCEDED,
      payload : data
      
    }
  }
export function clearChat(){
  return {
    type: CLEAR_CHAT
  }
}

export function predictionFailed(data) {
    return {
      type: PREDICTION_FAILED,
      payload: data
    }
  }


export function predictionRequested(data) {
    return {
      type: PREDICTION_REQUESTED,
      payload : data
    }
  }

export function sendTextAi(user, text) {
    return {
        type: SEND_TEXT_AI,
        payload: {
            text : text,
            user: user
        
        }
    }

}

