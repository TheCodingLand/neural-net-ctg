// This will be a display of the brain ot TINA. lets hope z
import React, { Component } from 'react';

import { connect } from "react-redux"
import Chip from 'material-ui/Chip';

function mapStateToProps(state) {
    return {
        user: state.user
    }

}



class Brain extends Component {
  render() {
      console.log(this.props)
      let br =""
      if (this.props.user.brain) {  br = this.props.user.brain.map((item) => { return <Chip label={item.category}/>})}

    return (
      <div>{br}
          </div>
    )}
}

export default connect(mapStateToProps)(Brain)