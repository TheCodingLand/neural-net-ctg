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
        case "SEND_TEXT_AI": {
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
        case "PREDICTION_SUCCEDED": {
            console.log("PREDICTION RECIEVED, updating chat")
            //CALL API
            

            state = { ...state, 
                conversationHistory: state.conversationHistory.concat({
                    id:state.conversationHistory.length,
                    user:'Tina',
                    content: 'I found a category with label ' + action.prediction.category + ' corresponding at your request'}) }
            console.log(state)
            return state
        }
        case "PREDICTION_FAILED": {
            console.log("PREDICTON FAILED")
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