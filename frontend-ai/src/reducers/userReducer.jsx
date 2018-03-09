const initialState = {
    userName: "",
    model: "",
    conversaionHistory: [],

}



export default function userReducer(state = initialState
    , action) {
    switch (action.type) {
        case "SEND_TEXT_AI": {
            console.log("SENDING TEXT")
            //CALL API

            //state = { ...state, progression: state.progression + 1 }
            console.log(state)
            return state
        }
        default:
            return state
    }
    return state

}