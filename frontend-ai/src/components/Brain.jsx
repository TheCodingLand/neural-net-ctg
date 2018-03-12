// This will be a display of the brain ot TINA. lets hope z
import React, { Component } from 'react';
import Reboot from 'material-ui/Reboot';
import { connect } from "react-redux"

function mapStateToProps(state) {
    return {
        user: state.user
    }

}



class Brain extends Component {
  render() {
      console.log(this.props)
      let br =""
      if (this.props.user.brain) {  br = this.props.user.brain.map((item) => { return 'thinking about ' + item.category})}

    return (
      <div>{br}
          </div>
    )}
}

export default connect(mapStateToProps)(Brain)