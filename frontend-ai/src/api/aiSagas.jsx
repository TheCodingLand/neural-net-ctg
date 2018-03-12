import { call, put, takeEvery, takeLatest } from 'redux-saga/effects'
import { chat_api, update_brain_api } from '../api/aiws'

// worker Saga: will be fired on USER_FETCH_REQUESTED actions
function* chat(action) {
   try {
      const chat = yield call(chat_api, action.payload.text);
      yield put({type: "CHAT_SUCCEEDED", chat: chat});
   } catch (e) {
      yield put({type: "CHAT_FAILED", message: e.message});
   }
}

function* updateBrain(action) {
  try {
     const prediction = yield call(update_brain_api, action.payload.text);
     yield put({type: "UPDATE_BRAIN_SUCCESS", prediction: prediction});
  } catch (e) {
     yield put({type: "UPDATE_BRAIN_FAILED", message: e.message});
  }
}

/*
  Starts fetchUser on each dispatched `USER_FETCH_REQUESTED` action.
  Allows concurrent fetches of user.
*/
function* aiSaga() {
  yield takeEvery("SEND_TEXT_CHAT", chat);
  yield takeLatest("CHAT_SUCCEEDED", updateBrain);
  
}

/*
  Alternatively you may use takeLatest.

  Does not allow concurrent fetches of user. If "USER_FETCH_REQUESTED" gets
  dispatched while a fetch is already pending, that pending fetch is cancelled
  and only the latest one will be run.

function* mySaga() {
  yield takeLatest("USER_FETCH_REQUESTED", fetchUser);
}
*/
export default aiSaga;