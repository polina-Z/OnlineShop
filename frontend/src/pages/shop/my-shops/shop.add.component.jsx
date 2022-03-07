import React from 'react';
import FormInput from '../../../components/form-input/form-input.component';
import CustomButton from '../../../components/custom-button/custom-button.component';

import './shop.add.styles.scss';

class ShopAdd extends React.Component {

    constructor(props) {
        super(props);
    
        this.state = {
          title: '',
          info: '',
          image: ''
        };
    };

    handleSubmit = async event => {
    };

    handleChange = event => {
        const { name, value } = event.target;

        this.setState({ [name]: value });
    };

    previewFile() {
        var  self  =  this;
        const file = document.querySelector('input[type=file]').files[0];
        const reader = new FileReader();
      
        reader.addEventListener("load", function () {
            self.setState({ image:  reader.result});
        }, false);
      
        if (file) {
          reader.readAsDataURL(file);
        };
    };

    render() {
        return (
            <div className='add'>
                <h2>Creat your shop</h2>
                <form onSubmit={this.handleSubmit}>
                    <FormInput
                        name='title'
                        type='title'
                        handleChange={this.handleChange}
                        value={this.state.title}
                        label='Shop title'
                        required
                    />
                    <div className="mb-3">
                        <label className="form-label">Select store image</label>
                        <input required className="form-control" type="file" id="formFile" onChange={this.previewFile.bind(this)}/>
                    </div>
                    <textarea name="info" className="form-controller" rows="3" onChange={this.handleChange}></textarea>
                    <div className="buttons">
                        <CustomButton type='submit'> CREATE</CustomButton>
                    </div>
                </form>
            </div>
        );
    }
}

export default ShopAdd;