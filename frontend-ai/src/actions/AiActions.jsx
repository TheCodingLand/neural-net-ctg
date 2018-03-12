
export const SEND_TEXT_CHAT = 'SEND_TEXT_CHAT'
export const CHAT_SUCCEEDED = 'CHAT_SUCCEEDED'
export const CHAT_FAILED = 'CHAT_FAILED'
export const SEND_CHAT_REQUESTED = 'SEND_CHAT_REQUESTED'
export const CLEAR_CHAT = 'CLEAR_CHAT'

export function sendChatSucceeded(data) {
  console.log('called action on prediction success')
    return {
      type: CHAT_SUCCEEDED,
      payload : data
      
    }
  }
export function clearChat(){
  return {
    type: CLEAR_CHAT
  }
}

export function sendChatFailed(data) {
    return {
      type: CHAT_FAILED,
      payload: data
    }
  }


export function sendChatRequested(data) {
    return {
      type: SEND_CHAT_REQUESTED,
      payload : data
    }
  }

export function sendTextChat(user, text) {
    return {
        type: SEND_TEXT_CHAT,
        payload: {
            text : text,
            user: user
        
        }
    }

}

