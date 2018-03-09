import { call, put, takeEvery, takeLatest } from 'redux-saga/effects'
import Api from '../api/aiws'

// worker Saga: will be fired on USER_FETCH_REQUESTED actions
function* predict(action) {
   try {
      const prediction = yield call(Api, action.payload.text);
      yield put({type: "PREDICTION_SUCCEDED", prediction: prediction});
   } catch (e) {
      yield put({type: "PREDICTION_FAILED", message: e.message});
   }
}

/*
  Starts fetchUser on each dispatched `USER_FETCH_REQUESTED` action.
  Allows concurrent fetches of user.
*/
function* aiSaga() {
  yield takeEvery("SEND_TEXT_AI", predict);
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