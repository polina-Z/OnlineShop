import React from "react";
import { withRouter } from 'react-router-dom';
import CustomButton from "../custom-button/custom-button.component";
import './myshop-item.styles.scss';

const ShopItem = ({title, image, info, history, match}) => (
    <div className="shop">
        <div>
            <h2>{title}</h2>
        </div>
        <div className="shop-item">
            <div 
                className='shop-image' 
                style={{
                backgroundImage: `url(${image})`
                }} 
            />
            <div className="text-container">{info}</div>
            <div className="container">
                <CustomButton>Edit Shop</CustomButton>
                <CustomButton>Add Category</CustomButton>
                <CustomButton>Add Product</CustomButton>
            </div>
        </div>
    </div>
);

export default withRouter(ShopItem);
