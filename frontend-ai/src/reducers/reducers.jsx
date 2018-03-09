import { combineReducers } from "redux"
import userReducer from "./userReducer"
//import bookmarkReducer from "./bookmarkReducer"

export default combineReducers(
    {
        user: userReducer,
    
    }
)
