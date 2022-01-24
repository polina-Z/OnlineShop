import { connect } from "react-redux";
import { createStructuredSelector } from "reselect";
import { compose } from "redux";
import { selectIsCollectionFetching } from "../../redux/directory/directory.selectors";
import WithSpinner from "../with-spinner/with-spinner.component";
import Directory from './directory.component';

const mapStateToProps = createStructuredSelector({
    isLoading: selectIsCollectionFetching
});

const DirectoryContainer = compose(
    connect(mapStateToProps),
    WithSpinner,
)(Directory);

export default DirectoryContainer;