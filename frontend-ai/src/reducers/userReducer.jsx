const initialState = {
    userName: "",
    model: "",

    conversationHistory: [
        {
        id: 0, 
        user: "Tina",
        content:"Hello, this is Tina, I can predit categories based on text input. please sent me text data, I'll answer. Currently I know only about Register of commerce issues."}]
        }


export default function userReducer(state = initialState
    , action) {
    switch (action.type) {
        case "SEND_TEXT_CHAT": {
            console.log("SENDING TEXT")
            //CALL API
            

            state = { ...state, 
                conversationHistory: state.conversationHistory.concat({
                    id:state.conversationHistory.length,
                    user:action.payload.user,
                    content:action.payload.text}) }
            console.log(state)
            return state
        
        }
        case "CLEAR_CHAT": {
            state = { ...state, conversationHistory : [ {
                id:0,
                user:'Tina',
                content:'Hello !'
            }]
            }
            return state
        }
        case "CHAT_SUCCEEDED": {
            console.log("SEND CHAT RECIEVED, updating chat")
            //CALL API
            

            state = { ...state, 
                conversationHistory: state.conversationHistory.concat({
                    id:state.conversationHistory.length,
                    user:'Tina',
                    content: action.prediction.category }) }
            console.log(state)
            return state
        }
        case "CHAT_FAILED": {
            console.log("SEND CHAT FAILED")
            //CALL API
            

            state = { ...state, 
                conversationHistory: state.conversationHistory.concat({
                    id:state.conversationHistory.length,
                    user:'Tina',
                    content:'sorry, api is not yet available for this question. please come back later !'}) }
            console.log(state)
            return state
        }
        default:
            return state
    }
    return state

}