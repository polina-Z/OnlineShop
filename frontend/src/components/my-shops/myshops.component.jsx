import React, { Component } from "react";
import ShopItem from "./myshop-item.component";
import { SmartRequest } from "../../utils/utils";
import { Link } from 'react-router-dom';
import CustomButton from "../custom-button/custom-button.component";
import './myshops.styles.scss';
import { withRouter } from 'react-router-dom';



class  MyShops extends Component { 
  constructor(props)
  {
    super(props);
    this.state = {
      shops: []
    }
  }

  componentDidMount() {
    SmartRequest.get('shop/myshop/')
                .then(resp => {
                    console.log('success in get shops info:', resp);
                    const shopsInfo = resp.data;
                    this.setState({shops: shopsInfo});
                });
  };

  render() {
    return (
      <div>
        <CustomButton onClick={() => {this.props.history.push('/shops/myshop/create')}}>Add Shop</CustomButton>
        <div className="shops-menu">
            {
                this.state.shops.map(({id, ...otherSectionProps}) => (
                <ShopItem key={id} {...otherSectionProps} />
            ))}
        </div>
      </div>
    )
  };
};

export default withRouter(MyShops);