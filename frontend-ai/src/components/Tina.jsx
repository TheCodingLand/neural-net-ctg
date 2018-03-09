import React, { Component } from 'react';
import Typography from 'material-ui/Typography';
import { withStyles } from 'material-ui/styles';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import TinaReplies from './TinaReplies'
import { sendTextAi } from '../actions/AiActions'
import { bindActionCreators } from "redux"
import { connect } from "react-redux"

const styles = theme => ({
    root: {
        position: "relative",
        flexGrow: 1,
        top:200
    },
    flex: {
        flex: 1,
    },
    menuButton: {
        marginLeft: -12,
        marginRight: 20,
    },
    loginButton: {
        float: 'right',
    },
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
        width: 200,
      },
});



class Tina extends Component {

    state = {


        multiline: '',
 
      };

    handleChange = name => event => {
        this.setState({
          [name]: event.target.value,
        });
      };

    handleSend() {
        this.props.sendTextAi("julien",this.state.multiline)
        this.setState(...this.state, {multiline:""})
    }
  render() {
      console.log(this.props)
    return (
    
      <div className={this.props.classes.root} >
       
        <TinaReplies conversation ={this.props.user.conversationHistory} />

       <TextField
          id="multiline-flexible"
          label="Reply"
          multiline
          rowsMax="4"
          value={this.state.multiline}
          onChange={this.handleChange('multiline')}
          className={this.props.classes.textField}
          margin="normal"
        />

                    <Button
                        variant="raised"
                        color="secondary"
                        onClick={this.handleSend.bind(this)}
                    >
                        Send
                    </Button>
      </div>
    );
  }
}


function mapStateToProps(state) {
    return {
        user: state.user
    }

}

function mapDispatchToProps(dispatch) {
    return bindActionCreators({
        sendTextAi,
    }, dispatch)


}

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(Tina))