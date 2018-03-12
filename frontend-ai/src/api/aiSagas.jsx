import { select, call, put, takeEvery, takeLatest } from 'redux-saga/effects'
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
     const conv = yield select();
     const updatedBrain = yield call(update_brain_api, conv.conversationHistory)
     yield put({type: "UPDATE_BRAIN", payload: updatedBrain});
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