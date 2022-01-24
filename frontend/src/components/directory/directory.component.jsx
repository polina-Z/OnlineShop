import React, { Component } from "react";
import MenuItem from '../menu-item/menu-item.component';
import './directory.styles.scss';
// import { connect } from 'react-redux';
// import { selectDirectorySections } from "../../redux/directory/directory.selectors";
// import { createStructuredSelector } from "reselect";
import CategoriesService from "../../services/categories/categories.service";

const  categoriesService  =  new  CategoriesService();


class  Directory extends Component { 
  constructor(props)
  {
    super(props);
    this.state = {
      sections: []
    };
  }

  componentDidMount() {
    var  self  =  this;
    categoriesService.getCategories().then(function (result) {
        console.log(result);
        if (result.length === 4){
          result[result.length - 1]["size"] = "large";
        }
        if (result.length === 5){
          result[result.length - 1]["size"] = "large";
          result[result.length - 2]["size"] = "large";
        }
        self.setState({ sections:  result});
    });
  }

  render() {
    return (
      <div className='directory-menu'>
          {
              this.state.sections.map(({id, ...otherSectionProps}) => (
              <MenuItem key={id} {...otherSectionProps} />
          ))}
      </div>
    )
  };
}

export default Directory;