const initialState = {
    userName: "",
    model: "",
    words: [{id: 0, word:"none", confidence:0},],
    brain: [ { id:0, category:"none", confidence :"0"}, ], 
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
            state = { ...state, 
                userName: "",
                model: "",
                words: [{id: 0, word:"none", confidence:0},],
                brain: [ { id:0, category:"none", confidence :"0"}, ], 
                conversationHistory: [
                    {
                    id: 0, 
                    user: "Tina",
                    content:"Hello, this is Tina, I can predit categories based on text input. please sent me text data, I'll answer. Currently I know only about Register of commerce issues."}]
                    }
            return state
        }
        case "UPDATE_BRAIN": {
            state = { ...state, brain : action.payload.results, words : action.payload.words
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
                    content: action.chat.response }) }
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
                    content:'I think i get it, is it one of those categories ?' }) }
            console.log(state)
            return state
        }
        default:
            return state
    }
    return state

}