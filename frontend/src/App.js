import React, {useEffect} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {Redirect, Route, Switch} from 'react-router-dom';
import HomePage from './pages/homepage/homepage.component';
import Header from './components/header/header.component';
import {setCurrentUserAsync} from './redux/user/user.actions';
import MyShopsPage from './pages/shop/my-shops/shops.page';
import {SmartRequest} from './utils/utils';
import ShopAdd from './pages/shop/my-shops/shop.add.component';
import SignInAndSignUpPage from './pages/sign-in-and-sign-up/sign-in-and-sign-up.component';
import CategoriesPage from './pages/shop/categories.component';
import CheckoutPage from './pages/checkout/checkout.component';
import './App.css';


const selectCurrentUser = state => state.user.currentUser;

function App() {
    const currentUser = useSelector(selectCurrentUser);
    const dispatch = useDispatch();

    useEffect(() => {
        if (currentUser) {
            SmartRequest.get('profile/')
                .then(resp => {
                    console.log('success in get profile:', resp)
                    const actualUser = resp.data
                    dispatch(setCurrentUserAsync(actualUser))
                });
        };
    });


    return (
        <div>
        <Header/>
        <Switch>
            <Route  path="/"  exact  component={HomePage}  />
            <Route path="/shops/myshop/create">
                {currentUser ? <ShopAdd/> : <Redirect to='/signin'/>}
            </Route>
            <Route path='/shops/myshop'>
                {currentUser ? <MyShopsPage/> : <Redirect to='/signin'/>}
            </Route>
            <Route exact path='/signin'>
                {currentUser ? <Redirect to='/'/> : <SignInAndSignUpPage/>}
            </Route>
            <Route path="/categories" component={CategoriesPage} />
            <Route exact path="/checkout" component={CheckoutPage} />
        </Switch>
      </div>
    );
};


export default App;
