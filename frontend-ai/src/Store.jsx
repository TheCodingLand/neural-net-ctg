import { applyMiddleware, createStore, subscribe } from "redux";

import logger from "redux-logger"
import thunk from "redux-thunk"
import promise from "redux-promise-middleware"
import reducers from "./reducers/reducers"
import { loadState, saveState } from './reducers/localStorage'
import createSagaMiddleware from 'redux-saga'
import aiSagas from './api/aiSagas'
const sagaMiddleware = createSagaMiddleware()
const persistedState = loadState();

let store = createStore(reducers, persistedState,applyMiddleware(logger,sagaMiddleware))
sagaMiddleware.run(aiSagas)
store.subscribe(() => {
    saveState(store.getState())
});


export default store