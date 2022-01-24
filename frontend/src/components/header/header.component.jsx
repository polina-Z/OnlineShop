import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { ReactComponent as Logo } from '../../assets/crown.svg';
import { createStructuredSelector } from 'reselect';
import { selectCartHidden } from '../../redux/cart/cart.selector';
import { selectCurrentUser } from '../../redux/user/user.selector';
import CartIcon from '../cart-icon/cart-icon.component';
import CartDropdown from '../cart/cart-dropdown/cart-dropdown.component';
import {setCurrentUserAsync} from '../../redux/user/user.actions';
import './header.styles.scss';
import { clearCart } from '../../redux/cart/cart.actions';


const Header = ({currentUser, hidden, signOutStart}) => (
  <div className='header'>
    <Link className='logo-container' to='/'>
      <Logo className='logo' />
    </Link>
    <div className='options'>
      { currentUser ?
        currentUser[0].store_owner ?
          <Link className='option' to='/shops/myshop'>
            MY SHOPS
          </Link> :
          <div></div>
          :
          <div></div>
      }
      <Link className='option' to='/shops'>
        SHOPS
      </Link>
      <Link className='option' to='/categories'>
        CATEGORIES
      </Link>
      {
        currentUser ?
        <div className='option' onClick={signOutStart}>
          SIGN OUT
        </div>
        :
        <Link className="option" to='/signin'>SIGN IN</Link>
      }
      <CartIcon />
    </div>
    {
      hidden ? null: 
      <CartDropdown />
    }
  </div>
);

const mapStateToProps = createStructuredSelector({
  hidden: selectCartHidden,
  currentUser: selectCurrentUser
});

const mapDispatchToProps = dispatch => ({
  signOutStart: () => {
    dispatch(setCurrentUserAsync(null));
    dispatch(clearCart());
  }
});

export default connect(mapStateToProps, mapDispatchToProps)(Header);