import {all, call} from 'redux-saga/effects';
import {watchSetCurrentUserAsync} from './user/user.sagas';
import {cartSagas} from './cart/cart.sagas';
import {shopSagas} from './shop/shop.sagas';

export default function* rootSaga() {
    yield all([
        watchSetCurrentUserAsync(),
        call(cartSagas),
        call(shopSagas)
    ]);
};
